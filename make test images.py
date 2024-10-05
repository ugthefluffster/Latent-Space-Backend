from PIL import Image, ImageDraw, ImageFont

# Define image properties
width, height = 512, 512
background_color = (0, 255, 0)  # Green background
text_color = (255, 0, 0)        # Red text

# Create 5 images with numbers 1 to 5
for i in range(1, 11):
    # Create a new image with green background
    img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(img)

    # Define font (default font if no custom font available)
    try:
        font = ImageFont.truetype("arial.ttf", 200)
    except IOError:
        font = ImageFont.load_default()

    # Calculate text size and position
    text = str(i)
    text_width, text_height = draw.textsize(text, font=font)
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2

    # Add the red number to the center of the image
    draw.text((text_x, text_y), text, fill=text_color, font=font)

    # Save the image
    img.save(f"images/{i}.jpg")

print("Images generated successfully!")
