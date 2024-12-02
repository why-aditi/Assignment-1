from flask import Flask, request, jsonify
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from pymongo import MongoClient

app = Flask(__name__)

load_dotenv()
DB_CONN = os.getenv('DB_CONN')

client = MongoClient(DB_CONN)
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
def trend():
    return jsonify({"message": "Trend endpoint is under construction."}), 200


if __name__ == '__main__':
    app.run(debug=True)
