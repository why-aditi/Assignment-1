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

@app.route("/data", methods=['GET'])  
def get_data():
    start_time = request.args.get('startTime')
    end_time = request.args.get('endTime')

    if not start_time or not end_time:
        return jsonify({"error": "startTime and endTime parameters are required"}), 400

    try:
        start_time = datetime.fromisoformat(start_time)
        end_time = datetime.fromisoformat(end_time)
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
    try: 
        duration = int(window[:-1])
        unit = window[-1]
    except ValueError:
        return jsonify({"error": "Invalid window format"}), 400
    
    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
        
    if unit =='m':
        end_time = start_time + relativedelta(months=duration)
    elif unit =='d':
        end_time = start_time + relativedelta(days=duration)
    elif unit =='h':
        end_time = start_time + relativedelta(hours=duration)
    
    query = {
        "Datetime": {
            "$gte": start_time,
            "$lte": end_time
        }
    }
    
    data = list(collection.find(query, {"_id": 0}))  
    
    count = 0
    for i in range(1, len(data)):
        datapoint = data[i]
        prev = data[i - 1][heading]
        if datapoint[heading] > prev:
            count += (datapoint[heading] - prev)
        elif datapoint[heading] < prev:
            count += (datapoint[heading] - prev)

    
    if count > 0:
        value = 'increases'
    elif count < 0:
        value = 'decreases'
    else:
        value = 'same'
    return jsonify({"datapoints": data, "value": value})
    
@app.route("/per-trend", methods=['GET'])  
def get_per_trend():
    start_time = request.args.get('startTime')
    window = request.args.get('window')
    heading = request.args.get('heading')
    try: 
        duration = int(window[:-1])
        unit = window[-1]
    except ValueError:
        return jsonify({"error": "Invalid window format"}), 400
    
    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
        
    if unit =='m':
        end_time = start_time + relativedelta(months=duration)
    elif unit =='d':
        end_time = start_time + relativedelta(days=duration)
    elif unit =='h':
        end_time = start_time + relativedelta(hours=duration)
    
    query = {
        "Datetime": {
            "$gte": start_time,
            "$lte": end_time
        }
    }
    
    data = list(collection.find(query, {"_id": 0}))  
    
    per = ((data[-1][heading] - data[0][heading])/data[0][heading])*100
    
    if per > 0:
        value = f"{abs(per):.2f}% increase"
    elif per < 0:
        value = f"{abs(per):.2f}% decrease"
    else: 
        value = 'same'
        
    return jsonify({"datapoints": data, "value": value})
    
    
if __name__ == '__main__':
    app.run(debug=True)
