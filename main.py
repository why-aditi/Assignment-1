from flask import Flask, request, jsonify
import datetime
from pymongo import MongoClient
from helper_function import analysis, compare, format, format_comp

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['JBM']
collection = db['Assignment1']  


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/data", methods=['GET'])
def get_data():
    start_time = request.args.get('startTime')
    end_time = request.args.get('endTime')

    if not start_time or not end_time:
        return jsonify({"error": "startTime and endTime parameters are required"}), 400

    try:
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return jsonify({"error": "Invalid datetime format. Use ISO format like 'YYYY-MM-DDTHH:MM:SS'"}), 400

    query = {
        "Datetime": {
            "$gte": start_time,
            "$lte": end_time
        }
    }

    data = list(collection.find(query, {"_id": 0}))  

    if not data:
        return jsonify({"message": "No data found for the given time range"}), 404

    return jsonify(data), 200


@app.route("/trend", methods=['GET'])  
def get_trend():
    start_time = request.args.get('startTime')
    window = request.args.get('window')
    heading = request.args.get('heading')
    datapoints = request.args.get('datapoints', 'true').lower()  

    start_time, end_time = format(start_time, window)

    query = {
        "Datetime": {
            "$gte": start_time,
            "$lte": end_time
        }
    }

    data = list(collection.find(query, {"_id": 0}))  

    if len(data) < 2:
        return jsonify({"error": "Not enough data points to calculate trend"}), 400

    value = analysis(data, heading)

    if datapoints == 'false':  
        return jsonify({"value": value})
    else:
        return jsonify({"datapoints": data, "value": value})


@app.route("/trend-compare", methods=['GET'])
def get_trend_compare():
    window1_start = request.args.get('window1_start')
    window2_start = request.args.get('window2_start')
    window1_end = request.args.get('window1_end')
    window2_end = request.args.get('window1_end')
    heading = request.args.get('heading')

    start_time1, end_time1 = format_comp(window1_start, window1_end)
    start_time2, end_time2 = format_comp(window2_start, window2_end)
    
    query1 = {"Datetime": {"$gte": start_time1, "$lte": end_time1}}
    query2 = {"Datetime": {"$gte": start_time2, "$lte": end_time2}}

    data1 = list(collection.find(query1, {"_id": 0}))
    data2 = list(collection.find(query2, {"_id": 0}))

    if len(data1) < 2 or len(data2) < 2:
        return jsonify({"error": "Not enough data points to calculate trend for one or both time windows"}), 400

    value = compare(data1, data2, heading)

    return jsonify(value)


if __name__ == '__main__':
    app.run(debug=True)
