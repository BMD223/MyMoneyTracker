from flask import Flask, jsonify, request
from source import update_prices

app = Flask(__name__)

stored_number = 42

@app.route('/get_number', methods=['GET'])
def get_number():
    """
    API endpoint to return the stored number.
    """
    return jsonify({"number": stored_number})

@app.route('/set_number', methods=['POST'])
def set_number():
    """
    API endpoint to update the stored number.
    """
    global stored_number
    data = request.get_json()
    if 'number' in data:
        stored_number = data['number']
        return jsonify({"message": "Number updated!", "number": stored_number}), 200
    return jsonify({"message": "Invalid request, 'number' is required"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
