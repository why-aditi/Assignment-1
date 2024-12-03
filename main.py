from flask import Flask, request, jsonify
import datetime
from pymongo import MongoClient
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['JBM']
collection = db['Assignment1']  

def analysis(data, heading):
    try:
        per = ((data[-1][heading] - data[0][heading]) / data[0][heading]) * 100
    except (KeyError, ZeroDivisionError):
        return {"error": f"Unable to calculate percentage change for heading '{heading}'"}, 400

    if per > 0:
        value = f"{abs(per):.2f}% increase"
    elif per < 0:
        value = f"{abs(per):.2f}% decrease"
    else: 
        value = 'same'

    return value


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

    try: 
        duration = int(window[:-1])
        unit = window[-1]
    except ValueError:
        return jsonify({"error": "Invalid window format. Use formats like '3d', '2m', '1h'"}), 400

    try:
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')  
    except ValueError:
        return jsonify({"error": "Invalid startTime format. Use 'YYYY-MM-DDTHH:MM:SS'"}), 400

    if unit == 'm':
        end_time = start_time + relativedelta(months=duration)
    elif unit == 'd':
        end_time = start_time + relativedelta(days=duration)
    elif unit == 'h':
        end_time = start_time + relativedelta(hours=duration)
    else:
        return jsonify({"error": "Invalid window unit. Use 'm', 'd', or 'h'"}), 400

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
    start_time1 = request.args.get('startTime1')
    start_time2 = request.args.get('startTime2')
    window = request.args.get('window')
    heading = request.args.get('heading')

    if not start_time1 or not start_time2:
        return jsonify({"error": "Both startTime1 and startTime2 parameters are required"}), 400

    try:
        start_time1 = datetime.datetime.strptime(start_time1, '%Y-%m-%dT%H:%M:%S')
        start_time2 = datetime.datetime.strptime(start_time2, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return jsonify({"error": "Invalid datetime format. Use 'YYYY-MM-DDTHH:MM:SS'"}), 400
    
    try:
        duration = int(window[:-1])
        unit = window[-1]
    except ValueError:
        return jsonify({"error": "Invalid window format. Use formats like '3d', '2m', '1h'"}), 400

    if unit == 'm':
        end_time1 = start_time1 + relativedelta(months=duration)
        end_time2 = start_time2 + relativedelta(months=duration)
    elif unit == 'd':
        end_time1 = start_time1 + relativedelta(days=duration)
        end_time2 = start_time2 + relativedelta(days=duration)
    elif unit == 'h':
        end_time1 = start_time1 + relativedelta(hours=duration)
        end_time2 = start_time2 + relativedelta(hours=duration)
    else:
        return jsonify({"error": "Invalid window unit. Use 'm', 'd', or 'h'"}), 400

    query1 = {"Datetime": {"$gte": start_time1, "$lte": end_time1}}
    query2 = {"Datetime": {"$gte": start_time2, "$lte": end_time2}}

    data1 = list(collection.find(query1, {"_id": 0}))
    data2 = list(collection.find(query2, {"_id": 0}))

    if len(data1) < 2 or len(data2) < 2:
        return jsonify({"error": "Not enough data points to calculate trend for one or both time windows"}), 400

    trend1 = analysis(data1, heading)
    trend2 = analysis(data2, heading)

    return jsonify({
        "trend1": trend1,
        "trend2": trend2,
        "window1_data": data1,
        "window2_data": data2
    })


if __name__ == '__main__':
    app.run(debug=True)
