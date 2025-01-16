from flask import Flask, jsonify, request
from source import get_total, add_positions
import pandas as pd

app = Flask(__name__)
pos_path = "/Users/bbd223/Desktop/Personal projects/private data/positions.csv"

stored_number = 42

@app.route('/update', methods=['GET'])
def update_number():
    """
    API endpoint to return the stored number.
    """
    values=get_total()
    original_value=values[0]
    current_value=values[1]
    
    return jsonify({"original_value": original_value,"current_value":current_value})

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

@app.route('/add_position', methods=['POST'])
def add_position():
    """
    Method that increases/decreases stored positions
    """
    path = "/Users/bbd223/Desktop/Personal projects/private data/positions.csv"
    data = request.get_json()  # Retrieve incoming JSON data
    print("Received data:", data)  # Debug: Print received data

    if not data:
        return jsonify({"message": "No data received!"}), 400

    df = pd.DataFrame([data])  # Wrap data in DataFrame
    add_positions(path, df)  # Call your function with the DataFrame
    return jsonify({"message": "Position added successfully!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6767)
