from flask import Flask, request, jsonify, send_file
import json
import os
from uuid import uuid4
from pyngrok import ngrok
from flask_cors import CORS
import random  

app = Flask(__name__)
CORS(app)

# Data storage file
DATA_FILE = 'game_data.json'

# Ensure data file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

# Endpoint to register a new game and get a UUID
@app.route('/register', methods=['POST'])
def register():
    # Generate a new UUID
    game_uuid = str(uuid4())

    # Save initial empty game data
    with open(DATA_FILE, 'r+') as f:
        data = json.load(f)
        data[game_uuid] = {}  # Initialize with empty data
        f.seek(0)
        json.dump(data, f)
        f.truncate()

    return jsonify({'uuid': game_uuid}), 200

# Endpoint to save game data
@app.route('/save', methods=['POST'])
def save_game():
    content = request.get_json()
    game_uuid = content.get('uuid')
    game_data = content.get('gameData')

    if not game_uuid or game_data is None:
        return jsonify({'error': 'Missing uuid or gameData'}), 400

    with open(DATA_FILE, 'r+') as f:
        data = json.load(f)
        data[game_uuid] = game_data
        f.seek(0)
        json.dump(data, f)
        f.truncate()

    return jsonify({'confirmation': 'Game data saved successfully.'}), 200

# Endpoint to load game data
@app.route('/load', methods=['POST'])
def load_game():
    content = request.get_json()
    game_uuid = content.get('uuid')

    if not game_uuid:
        return jsonify({'error': 'Missing uuid'}), 400

    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    game_data = data.get(game_uuid)

    if game_data is None:
        return jsonify({'error': 'Game data not found'}), 404

    return jsonify({'gameData': game_data}), 200

# Endpoint to reset game data
@app.route('/reset', methods=['POST'])
def reset_game():
    content = request.get_json()
    game_uuid = content.get('uuid')

    if not game_uuid:
        return jsonify({'error': 'Missing uuid'}), 400

    with open(DATA_FILE, 'r+') as f:
        data = json.load(f)
        if game_uuid in data:
            del data[game_uuid]
            f.seek(0)
            json.dump(data, f)
            f.truncate()
            return jsonify({'confirmation': 'Game data reset successfully.'}), 200
        else:
            return jsonify({'error': 'Game data not found'}), 404
        
@app.route('/getStarTexture', methods=['POST'])
def get_star_texture():
    content = request.get_json()
    game_uuid = content.get('uuid')
    position = content.get('position')

    if not game_uuid or position is None:
        return jsonify({'error': 'Missing uuid or position'}), 400

    # For printing purposes, let's print the position
    print(f"Received texture request for UUID {game_uuid}, position: {position}")

    # Convert the position to a string to use as a key (since JSON keys must be strings)
    position_key = json.dumps(position)

    with open(DATA_FILE, 'r+') as f:
        data = json.load(f)

        if game_uuid not in data:
            return jsonify({'error': 'Game data not found'}), 404

        game_data = data[game_uuid]

        # Ensure 'textures' field exists
        if 'textures' not in game_data:
            game_data['textures'] = {}

        textures = game_data['textures']

        # Check if position already has an assigned texture
        if position_key in textures:
            image_filename = textures[position_key]
        else:
            # Assign a random image
            image_filename = f"{random.randint(1,10)}.jpg"
            textures[position_key] = image_filename
            # Update the data file
            f.seek(0)
            json.dump(data, f)
            f.truncate()

        # Send the image file
        image_path = os.path.join('images', image_filename)  # assuming images are in 'images' folder

        if not os.path.exists(image_path):
            return jsonify({'error': f'Image file {image_filename} not found'}), 404

        return send_file(image_path, mimetype='image/jpeg')


if __name__ == '__main__':
    port = 5000

    # Start ngrok when the server starts
    ngrok_tunnel = ngrok.connect(port)
    public_url = ngrok_tunnel.public_url
    print(f" * ngrok tunnel available at {public_url}")
    app.config["BASE_URL"] = public_url
    try:
        app.run(port=port)
    finally:

        ngrok.kill() 


