from flask import Flask, request, jsonify
import datetime
from pymongo import MongoClient
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['JBM']
collection = db['Assignment1']  

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

from datetime import datetime
from flask import jsonify, request

@app.route("/data", methods=['GET'])
def get_data():
    start_time = request.args.get('startTime')
    end_time = request.args.get('endTime')

    if not start_time or not end_time:
        return jsonify({"error": "startTime and endTime parameters are required"}), 400

    try:
        start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
        end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")
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
        start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')  # Use the correct datetime class
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

    try:
        per = ((data[-1][heading] - data[0][heading]) / data[0][heading]) * 100
    except (KeyError, ZeroDivisionError):
        return jsonify({"error": f"Unable to calculate percentage change for heading '{heading}'"}), 400

    if per > 0:
        value = f"{abs(per):.2f}% increase"
    elif per < 0:
        value = f"{abs(per):.2f}% decrease"
    else: 
        value = 'same'

    if datapoints == 'false':  
        return jsonify({"value": value})
    else:
        return jsonify({"datapoints": data, "value": value})

    

@app.route('/compare-windows', methods=['GET'])
def compare_windows():
    start_time1 = request.args.get('startTime1')
    start_time2 = request.args.get('startTime2')
    window = request.args.get('window')
    heading = request.args.get('heading')
        
    return jsonify({"value": value})

if __name__ == '__main__':
    app.run(debug=True)
