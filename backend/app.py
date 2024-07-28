import os
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
import boto3
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/flight_db"
mongo = PyMongo(app)

sns_client = boto3.client(
    'sns',
    region_name='ap-south-1',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

SNS_TOPIC_ARN = 'arn:aws:sns:ap-south-1:127970141488:FlightStatusUpdates'

@app.route('/api/flights', methods=['GET'])
def get_flights():
    flights = mongo.db.flights.find()
    response = dumps(flights)
    return response

@app.route('/update-flight-status', methods=['POST'])
def update_flight_status():
    data = request.json
    flight_number = data.get('flightNumber')
    status = data.get('status')

    mongo.db.flights.update_one(
        {"flightNumber": flight_number},
        {"$set": {"status": status}}
    )

    response = sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=f'Flight {flight_number} status updated to {status}',
        Subject='Flight Status Update'
    )

    return jsonify({"message": "Notification sent", "response": response})

if __name__ == '__main__':
    app.run(debug=True)
