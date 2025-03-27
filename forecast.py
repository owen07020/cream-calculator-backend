from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins=["https://cream-calculator-frontend.vercel.app"])

@app.route('/api/forecast', methods=['POST'])
def forecast():
    try:
        data = request.get_json()
        return jsonify({"status": "working", "data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


