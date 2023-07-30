import boto3
import json
import os
import sys

session = boto3.Session(profile_name='bedrock')
boto3_bedrock = session.client('bedrock', 'us-east-1', endpoint_url='https://bedrock.us-east-1.amazonaws.com')

import io, base64
from PIL import Image

prompt = "White cat in a forest with clear background"
negative_prompts = [
    "poorly rendered", 
    "poor background details", 
    "poorly drawn", 
    "disfigured cat features"
    ]
style_preset = "photographic" # (photographic, digital-art, cinematic, ...)

module_path = "."
sys.path.append(os.path.abspath(module_path))
import bedrock
model = bedrock.Bedrock(boto3_bedrock)
base_64_img_str = model.generate_image(prompt, cfg_scale=5, seed=5450, steps=70, style_preset=style_preset)

image_1 = Image.open(io.BytesIO(base64.decodebytes(bytes(base_64_img_str, "utf-8"))))

# Save the image in the same directory as the code
image_filename = "generated_image.jpg"
image_1.save(image_filename)

print(f"Image saved as {image_filename}")