from flask import Flask, request, jsonify
from flasgger import Swagger
import pickle
import numpy as np
import random
import logging
import os  
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
swagger = Swagger(app)

# Load the fraud detection model
with open('fraud_detection_xgboost.pkl', 'rb') as file:
    model = pickle.load(file)

# Load additional model for deception detection (if required)
with open('fraud_detection_xgboost.pkl', 'rb') as file:
    deception_model = pickle.load(file)

# Configure logging for deception tracking
logging.basicConfig(filename="deception_log.log", level=logging.INFO)

# Create honeypot transactions (synthetic fraudulent transactions)
HONEYPOT_TRANSACTIONS = [
    [random.uniform(0, 1) for _ in range(30)]  # Match the feature count
    for _ in range(5)
]

# Flask Limiter to detect high request rates
limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])

# Dictionary to track suspicious users
suspicious_users = {}

# Honeypot keys
honeypot_keys = ["honeypot1", "honeypot2", "trap_feature", "hidden_flag"]

@app.route('/predict', methods=['POST'])
@limiter.limit("5 per minute")  # Limit to 5 requests per minute per IP
def predict():
    """
    Predict whether a transaction is fraudulent or not.
    ---
    parameters:
      - name: features
        in: body
        required: true
        schema:
          type: object
          properties:
            features:
              type: array
              items:
                type: number
    responses:
      200:
        description: The model's fraud prediction
    """
    data = request.get_json()
    user_ip = request.remote_addr

    if 'features' not in data:
        return jsonify({"error": "Missing 'features' in request data"}), 400

    try:
        features = np.array(data['features']).reshape(1, -1)
    except Exception as e:
        return jsonify({"error": f"Invalid feature format: {str(e)}"}), 400

    # Honeypot detection
    if any(key in data for key in honeypot_keys) or features.tolist() in HONEYPOT_TRANSACTIONS:
        logging.info(f"Honeypot triggered from IP {user_ip}: {data}")
        suspicious_users[user_ip] = {
            'count': suspicious_users.get(user_ip, {}).get('count', 0) + 1
        }
        return jsonify({"error": "Access denied due to suspicious activity."}), 403

    # Repeated suspicious activity
    if user_ip in suspicious_users and suspicious_users[user_ip]['count'] > 3:
        logging.info(f"Blocking {user_ip} due to repeated suspicious activity.")
        return jsonify({'error': "Access denied due to suspicious activity."}), 403

    # Make prediction
    prediction = model.predict(features)

    # Monitor repetitive safe traffic
    if prediction[0] == 0:
        if user_ip not in suspicious_users:
            suspicious_users[user_ip] = {'count': 0}
        suspicious_users[user_ip]['count'] += 1
        if suspicious_users[user_ip]['count'] > 3:
            logging.info(f"Suspicious repeated normal queries from {user_ip}")

    return jsonify({'fraud_prediction': int(prediction[0])})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
