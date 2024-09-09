from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from message import create_mail, send_email
from booking_id import generate_booking_id  # Import function correctly


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
#app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'

mail = create_mail(app)  # Pass the app instance to create_mail

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    # Extract parameters from the request
    parameters = req.get('queryResult', {}).get('parameters', {})
    email_address = parameters.get('email')
    adult_count = parameters.get('adultcount')
    child_count = parameters.get('childcount')

    # Check for missing parameters and convert lists to integers
    if not email_address:
        return jsonify({'fulfillmentText': 'Please provide your email address.'})
    
    if not adult_count or not child_count:
        return jsonify({'fulfillmentText': 'Please provide the number of adults and children.'})
    
    # Convert to integers if they are lists or strings
    try:
        adult_count = int(adult_count[0]) if isinstance(adult_count, list) else int(adult_count)
        child_count = int(child_count[0]) if isinstance(child_count, list) else int(child_count)
    except (ValueError, TypeError) as e:
        return jsonify({'fulfillmentText': 'Invalid input for the number of adults or children.'})

    # Define costs
    cost_per_adult = 15
    cost_per_child = 10

    # Calculate total amount
    total_amount = (adult_count * cost_per_adult) + (child_count * cost_per_child)
    booking_id = generate_booking_id()

    # Send email with the calculated total amount
    send_email(mail, app.config, email_address, adult_count, child_count, cost_per_adult, cost_per_child, total_amount, booking_id)  # Pass app.config to send_email

    return jsonify({'fulfillmentText': f'Booking ID: {booking_id}. Email sent successfully with the total amount and payment link.'})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
