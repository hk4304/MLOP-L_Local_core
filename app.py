from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Load the model
model_path = 'models/model.joblib'
model = None

if os.path.exists(model_path):
    model = joblib.load(model_path)
    print(f"Model loaded successfully from {model_path}")
else:
    print(f"Warning: Model not found at {model_path}")

@app.route('/')
def home():
    return jsonify({
        "message": "Volunteer Turnout Prediction API",
        "status": "running",
        "model_loaded": model is not None,
        "endpoints": ["/", "/health", "/predict"]
    })

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    try:
        data = request.json
        df = pd.DataFrame([data])
        prediction = model.predict(df)
        return jsonify({
            "prediction": float(prediction[0]),
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
