from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Relworx API configuration
RELWORX_API_KEY = os.getenv('RELWORX_API_KEY')
RELWORX_MERCHANT_ID = os.getenv('RELWORX_MERCHANT_ID')
RELWORX_BASE_URL = 'https://api.relworx.com/v1'  # Replace with actual API URL

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/initiate-payment', methods=['POST'])
def initiate_payment():
    try:
        data = request.json
        amount = data.get('amount')
        currency = data.get('currency', 'USD')
        reference = data.get('reference')

        if not all([amount, reference]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Prepare payment request to Relworx
        headers = {
            'Authorization': f'Bearer {RELWORX_API_KEY}',
            'Content-Type': 'application/json'
        }

        payload = {
            'merchant_id': RELWORX_MERCHANT_ID,
            'amount': amount,
            'currency': currency,
            'reference': reference,
            'callback_url': request.host_url + 'payment-callback'
        }

        # Make request to Relworx API
        response = requests.post(
            f'{RELWORX_BASE_URL}/payments',
            json=payload,
            headers=headers
        )

        return jsonify(response.json())

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/payment-callback', methods=['POST'])
def payment_callback():
    try:
        # Verify the payment callback
        data = request.json
        
        # Verify signature (implement according to Relworx documentation)
        # Process the payment status
        
        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/check-payment-status/<payment_id>', methods=['GET'])
def check_payment_status(payment_id):
    try:
        headers = {
            'Authorization': f'Bearer {RELWORX_API_KEY}',
            'Content-Type': 'application/json'
        }

        response = requests.get(
            f'{RELWORX_BASE_URL}/payments/{payment_id}',
            headers=headers
        )

        return jsonify(response.json())

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not all([RELWORX_API_KEY, RELWORX_MERCHANT_ID]):
        print("Error: Missing required environment variables")
        exit(1)
    
    app.run(debug=True) 