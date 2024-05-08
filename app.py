"""Module providing REST API for generating challan."""
import os
import json
from confluent_kafka import Producer
import socket
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

# Publish message to Kafka
def PublishChallan(challanMsg):
    # Publish message to kafka topic
    producer.produce('Challan', value=challanMsg)

    # Wait for publish to complete
    producer.flush()
         
# Create Flask app
app = Flask(__name__)

# about page
@app.route('/about')
def about():
    """ Function that show application information."""
    
    # Render the page with application information
    return render_template('about.html')

# index page
@app.route('/', methods=('GET', 'POST'))
def index():
    """ Function that allows to  generate a challan."""
    # Check for POST method
    if request.method == 'POST':
        # Vehicle Number is mandatory
        if not request.form['vehicle_number']:
            flash('Vehicle Number is required!')

        else:    
            # Get challan attributes
            challanDict = { 'Vehicle Number': request.form['vehicle_number'],
                            'Unit Name': request.form['unit_name'],
                            'Date': request.form['date'],
                            'Time': request.form['time'],
                            'Place of Violation': request.form['place_of_violation'],
                            'PS Limits' : request.form['ps_limits'],
                            'Violation': request.form['violation'],
                            'Fine Amount': request.form['fine_amount'] }
            
            # Publish message to Kafka
            PublishChallan(json.dumps(challanDict))

            # Show a publish popup message
            flash(f"Challan for vehicle \"{request.form['vehicle_number']}\" is generated!") 
            
    # Render index page
    return render_template('index.html')

# Starts from here
if __name__ == "__main__":   
    # Initialize kafka configuration
    conf = {'bootstrap.servers': os.getenv('KAFKA_SERVICE_HOST') + ':' + os.getenv('KAFKA_SERVICE_PORT'),
            'client.id': socket.gethostname()}

    # Create  a producer
    producer = Producer(conf)

    # Set the configuration
    app.config[os.getenv("FLASK_KEY")] = os.getenv("FLASK_KEY_VALUE")

    # Run the application
    app.run(host='0.0.0.0', port=8003)