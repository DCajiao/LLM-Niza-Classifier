from flask import Flask, request, jsonify
from flask_cors import CORS

from core.app import get_classification_niza
from security.api_key_management import require_api_key

app = Flask(__name__)
CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization", "x-api-key"]
}})

@app.route('/predict_niza_classification', methods=['POST', 'OPTIONS'])
@require_api_key
def form_submission():
    if request.method == 'OPTIONS':
        return '', 200 # Empty response for preflight
    
    data = request.get_json()
    
    if 'description' not in data or not data['description']:
        # Return an error response if the field is missing or empty
        return jsonify({"error": "Missing 'description' field"}), 40

    try:
        response = get_classification_niza(data['description'])
        print(f"Respuesta del modelo: {response}")

        if response["clasificaciones"][0]['clase'] == "Error":
            return jsonify({"error": response["message"]}), 400
        else:
            return jsonify({"message": response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['POST'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
