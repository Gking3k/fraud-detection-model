import requests
import pandas as pd
import json

# Load simulated First Bank transactions
df = pd.read_csv("firstbank_transactions.csv")

url = "http://127.0.0.1:5000/predict"

fraud_count = 0
total = len(df)

print(" Sending First Bank transactions to the model...\n")

for _, row in df.iterrows():
    features = row.drop(labels=["Class"], errors='ignore').tolist()
    payload = {"features": features}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            prediction = response.json().get("fraud_prediction")
            if prediction == 1:
                fraud_count += 1
    except Exception as e:
        print(" Error:", e)

# Report results
print(" TOTAL Transactions Tested:", total)
print(" Fraudulent Transactions Detected:", fraud_count)
print(" Legitimate Transactions:", total - fraud_count)
print("\n Fraud Rate: {:.2f}%".format((fraud_count / total) * 100))
