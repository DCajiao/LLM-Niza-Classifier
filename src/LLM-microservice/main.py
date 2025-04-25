from flask import Flask, request, jsonify

from core.app import get_classification_niza
from security.api_key_management import require_api_key

app = Flask(__name__)


@app.route('/predict_niza_classification', methods=['POST'])
@require_api_key
def form_submission():
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
