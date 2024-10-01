import requests
import numpy as np
from PIL import Image
from io import BytesIO

# Replace with your public_url
base_url = "https://3ce7-34-124-163-51.ngrok-free.app"

# Scaling factor for standard normal distribution
sigma = 333333  # Approximately scales to ±1,000,000 at 3σ

# Register a player
response = requests.post(f"{base_url}/register")
print("Registration Response:", response.json())

# Check if the server is initialized
if response.json().get('status') == 'ok':
    game_id = response.json().get('game_id')
    
    coords = None  # Variable to store coordinates of the 3rd image

    # Function to generate Gaussian coordinates
    def generate_gaussian_coords(game_id, sigma):
        return {
            'game_id': game_id,
            'x': int(np.random.normal(0, sigma)),
            'y': int(np.random.normal(0, sigma)),
            'z': int(np.random.normal(0, sigma)),
            'w': int(np.random.normal(0, sigma)),
            'v': int(np.random.normal(0, sigma))
        }

    # Retrieve 3 images with random coordinates following a standard normal distribution
    for i in range(3):
        # Generate random coordinates using Gaussian distribution
        coords = generate_gaussian_coords(game_id, sigma)
        print(f"\nRequesting image {i+1} with coordinates: {coords}")

        # Request an image
        image_response = requests.get(f"{base_url}/get_image", params=coords)
        if image_response.status_code == 200:
            # Open the image using PIL
            img = Image.open(BytesIO(image_response.content))
            # img.show()  # Uncomment if you want to display the image

            # Save the image to a file
            img_filename = f"downloaded_image_{i+1}.png"
            img.save(img_filename)
            print(f"Image {i+1} saved as {img_filename}")
        else:
            print(f"Failed to get image {i+1}:", image_response.text)
    
    # Now retrieve the last image 2 more times with the same coordinates
    for i in range(4, 6):  # Images 4 and 5
        print(f"\nRequesting image {i} with the same coordinates as image 3: {coords}")

        # Request the image with the same coordinates
        image_response = requests.get(f"{base_url}/get_image", params=coords)
        if image_response.status_code == 200:
            # Open the image using PIL
            img = Image.open(BytesIO(image_response.content))
            # img.show()  # Uncomment if you want to display the image

            # Save the image to a file
            img_filename = f"downloaded_image_{i}.png"
            img.save(img_filename)
            print(f"Image {i} saved as {img_filename}")
        else:
            print(f"Failed to get image {i}:", image_response.text)
else:
    print("Server is initializing. Please wait.")
