import requests
import os
import json

# Set the base URL for the server (adjust the port if needed)
BASE_URL = "https://cb8c-35-240-229-36.ngrok-free.app"

# Step 1: Register a new game and retrieve the UUID
def register_game():
    response = requests.post(f"{BASE_URL}/register")
    if response.status_code == 200:
        uuid = response.json().get('uuid')
        print(f"Game registered with UUID: {uuid}")
        return uuid
    else:
        print("Failed to register game.")
        return None

# Step 2: Request a star texture with specific coordinates
def request_star_texture(uuid, position):
    payload = {
        'uuid': uuid,
        'position': position
    }
    
    response = requests.post(f"{BASE_URL}/getStarTexture", json=payload)
    
    if response.status_code == 200:
        print("Image received, saving to file.")
        with open('star_texture.jpg', 'wb') as f:
            f.write(response.content)
        print("Image saved as 'star_texture.jpg'")
    else:
        print(f"Failed to retrieve texture: {response.status_code}, {response.json()}")

# Step 3: Test the flow
if __name__ == "__main__":
    # Register the game
    game_uuid = register_game()
    
    if game_uuid:
        for i in range(1,5):
            # Request a star texture with coordinates (example: [1000000, -500000])
            position = [i*100000, 0, 0, 0, 0]
            request_star_texture(game_uuid, position)
