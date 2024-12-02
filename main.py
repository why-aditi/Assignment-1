from flask import Flask, request, jsonify
from datetime import datetime
import pandas as pd
from pymongo import MongoClient

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
    window = request.args.get('window')
    try: 
        duration = int(window[:-1])
        unit = window[-1]
    except ValueError:
        return jsonify({"error": "Invalid window format"}), 400
    
    max_time_entry = collection.find_one(
        sort=[("Datetime", -1)],  
        projection={"Datetime": 1, "_id": 0} 
    )    
    end_time = max_time_entry["Datetime"]
    if isinstance(end_time, str):
        end_time = datetime.fromisoformat(end_time)
        
    if unit =='m':
        start_time = end_time - pd.Timedelta(weeks=duration*4)
    elif unit =='d':
        start_time = end_time - pd.Timedelta(days=duration)
    elif unit =='h':
        start_time = end_time - pd.Timedelta(hours=duration)
    
    query = {
        "Datetime": {
            "$gte": start_time,
            "$lte": end_time
        }
    }
    
    data = list(collection.find(query, {"_id": 0}))  
    
    for i in range(1, len(data)):
        datapoint = data[i]
        count = 0
        prev = data[i-1]['PT08']['S1(CO)']
        if datapoint['PT08']['S1(CO)'] > prev:
            count += 1
        elif datapoint['PT08']['S1(CO)'] < prev:
            count -= 1
        else:
            continue
    
    if count > 0:
        value = 'increases'
    elif count < 0:
        value = 'decreases'
    else:
        value = 'same'
    return jsonify({"datapoints": len(data), "value": value})
    
if __name__ == '__main__':
    app.run(debug=True)
