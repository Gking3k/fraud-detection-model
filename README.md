# A Deception Model for Combating Malicious Activities in Financial Data

This is a complete fraud detection model integrated with deception techniques, built using Python and Flask. It demonstrates fraud detection using a trained XGBoost model and includes honeypot-based deception techniques for detecting malicious activity. A case study using simulated First Bank Nigeria data is also included.

# Project Contents

- `app.py` — Main Flask API application.
- `fraud_detection_xgboost.pkl` — Trained fraud detection model.
- `creditcard.csv` — Dataset used to train the model (derived from kaggle).
- `firstbank_transactions.csv` — Simulated case study data (First Bank of Nigeria).
- `evaluate_firstbank.py` — Code to test model using First Bank data.
- `test_normal_requests.py` — Script to simulate normal user transactions.
- `test_deception_protection.py` — Script to simulate deception detection (honeypots, suspicious behavior).
- `requirements.txt` — All project dependencies.
- `README.md` — This instruction file.

# How to Set Up and Run the Project

# 1. Install Python (Version 3.10 or later)
Download and install Python from the official website:
- https://www.python.org/downloads/

> Make sure Python is added to your system PATH.

# 2. Create and Activate a Virtual Environment
Open Command Prompt (Windows) or Terminal (Mac/Linux) and navigate to the folder where the project files are located.
Then run:
# For **Windows**:
```bash
python -m venv venv
.\venv\Scripts\activate
```

# For **Mac/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

# 3. Install Required Dependencies
Make sure you are in the project folder and the virtual environment is activated. Then in the same Command Prompt or Terminal window,
run:

```bash
pip install -r requirements.txt
```

This will install Flask, XGBoost, pandas, scikit-learn, and other required libraries.

# 4. Run the Flask Application (Start the API)
Once setup is complete, start the backend API server in Command Prompt or Teminal Window with:

```bash
python app.py
```

# You should see a message like:
```
* Running on http://127.0.0.1:5000
```
The API is now running and ready to receive requests.
Copy and paste http://127.0.0.1:5000 into your web browser to access the API.

# If it doesn’t open:

-Check that your firewall or antivirus isn’t blocking Python.

-Ensure you're using the correct Python version and environment.

-Try localhost:5000 in the browser instead.

-If still not opening trying changing the port

# To change the Flask server port from the default 5000 to something like 8000, follow these steps:

- Open your app.py file.

- Locate the line where the app runs: 

   *app.run()

 # Modify it to specify the port you want: 
  
  *app.run(port=8000)

# How to Test Using Swagger UI (Flasgger)
Once the Flask app is running, go to:

http://127.0.0.1:5000/apidocs
This will open a page where you can test the API directly in your browser.

# Steps to Test
i. Click on the /predict endpoint.

ii. Click the “Try it out” button.

iii. In the “Request body”, paste one of the test samples.

# Where to Get Sample Test Payloads:
Use the values from these files included in this project:

test_normal_requests.py	- Normal (non-fraudulent) test data
test_deception_protection.py - Suspicious test data with honeypot keys

# Sample Payloads Format:
Copy a row from the Excel file and paste it using commas in this format:

{
  "features": [value1, value2, value3, ..., value30]
}

For deception tests, also include honeypot keys:

{
  "features": [value1, value2, value3, ..., value30],
  "honeypot1": 9999,
  "honeypot2": 660295
}

# Expected Outcome

"fraud_prediction": 0	- Legitimate transaction

"fraud_prediction": 1	- Fraudulent transaction 

403 Forbidden	- Deception or suspicious activity was detected

# 5. Interact with the Fraud Detection System
Once the flask app is running you can now interact with the system using one of the test scripts.

#  Test with First Bank Case Study
In Command Prompt or Terminal Window run:
```bash
python evaluate_firstbank.py
```
This test sends 3,000 transactions and shows how many were flagged as fraud.

#  Simulate Normal User Requests
In Command Prompt or Terminal Window run:
```bash
python test_normal_requests.py
```
This script tests how legitimate users are treated by the system.

#  Simulate Deception and Honeypot Detection
In Command Prompt or Terminal Window run:
```bash
python test_deception_protection.py
```
This will trigger deception techniques and show how the system reacts to suspicious behavior.

#  Case Study and Dataset
- The model was trained on `creditcard.csv`, a real-world dataset of financial transactions (derived from kaggle).
- `firstbank_transactions.csv` contains simulated transactions from First Bank of Nigeria and serves as a case study.


#  What to Expect
- After running the tests, you will see total transactions tested, number of fraudulent transactions detected, and insights.
- The system uses deception mechanisms like honeypots and IP tracking to catch malicious users.
