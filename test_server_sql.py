from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
import os
from uuid import uuid4
from pyngrok import ngrok
from flask_cors import CORS
import random
import json

app = Flask(__name__)
CORS(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class GameData(db.Model):
    __tablename__ = 'game_data'
    uuid = db.Column(db.String(36), primary_key=True)  # UUIDs are 36 characters
    data = db.Column(db.JSON)  # Stores the game data as JSON

    textures = db.relationship('Texture', backref='game_data', lazy=True)

class Texture(db.Model):
    __tablename__ = 'textures'
    id = db.Column(db.Integer, primary_key=True)
    game_uuid = db.Column(db.String(36), db.ForeignKey('game_data.uuid'), nullable=False)
    position_key = db.Column(db.String, nullable=False)
    image_filename = db.Column(db.String, nullable=False)

@app.route('/register', methods=['POST'])
def register():
    # Generate a new UUID
    game_uuid = str(uuid4())

    # Save initial empty game data
    new_game = GameData(uuid=game_uuid, data={})
    db.session.add(new_game)
    db.session.commit()

    return jsonify({'uuid': game_uuid}), 200

@app.route('/save', methods=['POST'])
def save_game():
    content = request.get_json()
    game_uuid = content.get('uuid')
    game_data = content.get('gameData')

    if not game_uuid or game_data is None:
        return jsonify({'error': 'Missing uuid or gameData'}), 400

    game = GameData.query.get(game_uuid)
    if not game:
        return jsonify({'error': 'Game data not found'}), 404

    game.data = game_data
    db.session.commit()

    return jsonify({'confirmation': 'Game data saved successfully.'}), 200

@app.route('/load', methods=['POST'])
def load_game():
    content = request.get_json()
    game_uuid = content.get('uuid')

    if not game_uuid:
        return jsonify({'error': 'Missing uuid'}), 400

    game = GameData.query.get(game_uuid)
    if not game:
        return jsonify({'error': 'Game data not found'}), 404

    return jsonify({'gameData': game.data}), 200

@app.route('/reset', methods=['POST'])
def reset_game():
    content = request.get_json()
    game_uuid = content.get('uuid')

    if not game_uuid:
        return jsonify({'error': 'Missing uuid'}), 400

    game = GameData.query.get(game_uuid)
    if game:
        # Delete associated textures
        Texture.query.filter_by(game_uuid=game_uuid).delete()
        # Delete the game data
        db.session.delete(game)
        db.session.commit()
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

    # Convert the position to a string to use as a key
    position_key = json.dumps(position)

    game = GameData.query.get(game_uuid)
    if not game:
        return jsonify({'error': 'Game data not found'}), 404

    # Check if texture already exists for this position
    texture = Texture.query.filter_by(game_uuid=game_uuid, position_key=position_key).first()

    if texture:
        image_filename = texture.image_filename
    else:
        # Assign a random image
        image_filename = f"{random.randint(1,10)}.jpg"
        new_texture = Texture(game_uuid=game_uuid, position_key=position_key, image_filename=image_filename)
        db.session.add(new_texture)
        db.session.commit()

    # Send the image file
    image_path = os.path.join('images', image_filename)  # assuming images are in 'images' folder

    if not os.path.exists(image_path):
        return jsonify({'error': f'Image file {image_filename} not found'}), 404

    return send_file(image_path, mimetype='image/jpeg')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
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
