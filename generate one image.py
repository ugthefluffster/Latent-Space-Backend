# generate one image with given scale values

scales = {
    'color': -1.7,
    'size': -1.8,
    'shape': 0.53,
    'brightness': -0.48,
    'material': 0.2,
}

image = slider.generate(
    prompt="a photo of a house",
    scales=scales,
    seed=15,
    num_inference_steps=20,
)

file_name = "image_" + "_".join([f"{key}_{value}" for key, value in scales.items()]) + ".png"
image[0].save(file_name)