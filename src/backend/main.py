from flask import Flask, request, jsonify
from flask_cors import CORS

from core.app import insert_data
from security.api_key_management import require_api_key

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["POST", "OPTIONS"], allow_headers=["Content-Type", "Authorization", "x-api-key"])


@app.route('/form_submission', methods=['POST'])
@require_api_key
def form_submission():
    data = request.get_json()
    try:
        response = insert_data(data)

        if response["status"] == "error":
            return jsonify({"error": response["message"]}), 400
        elif response["status"] == "success":
            return jsonify({"message": response["message"]}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['POST'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
