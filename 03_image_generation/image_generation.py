import boto3
import json
import os
import sys
import argparse

session = boto3.Session(profile_name='bedrock')
boto3_bedrock = session.client('bedrock', 'us-east-1', endpoint_url='https://bedrock.us-east-1.amazonaws.com')

import io, base64
from PIL import Image

parser = argparse.ArgumentParser(description='Process some inputs.')
parser.add_argument('--prompt', type=str, required=True, help='Main prompt')
parser.add_argument('--negative_prompts', type=str, nargs='+', required=True, help='List of negative prompts')
parser.add_argument('--style_preset', type=str, choices=['photographic', 'digital-art', 'cinematic'], required=True, help='Style preset')
args = parser.parse_args()

prompt = args.prompt
negative_prompts = args.negative_prompts
style_preset = args.style_preset

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
