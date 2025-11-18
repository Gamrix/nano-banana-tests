#!/usr/bin/env python3
"""Test API to see what's happening"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

print("Testing image generation...")
print()

try:
    # Test 1: Try with dall-e-3 (known to work)
    print("Test 1: dall-e-3 without extra params")
    response = client.images.generate(
        model="dall-e-3",
        prompt="A simple red circle on white background",
        n=1,
        size="1024x1024",
    )
    print(f"Success! URL: {response.data[0].url}")
    print()
except Exception as e:
    print(f"Failed: {e}")
    print()

try:
    # Test 2: Try with gpt-image-1
    print("Test 2: gpt-image-1 without extra params")
    response = client.images.generate(
        model="gpt-image-1",
        prompt="A simple red circle on white background",
        n=1,
        size="1024x1024",
    )
    print(f"URL: {response.data[0].url}")
    print(f"B64 JSON: {response.data[0].b64_json is not None}")
    if response.data[0].b64_json:
        print(f"B64 JSON length: {len(response.data[0].b64_json)}")
    print()
except Exception as e:
    print(f"Failed: {e}")
    print()

try:
    # Test 3: Try with gpt-image-1 and quality param
    print("Test 3: gpt-image-1 with quality param")
    response = client.images.generate(
        model="gpt-image-1",
        prompt="A simple red circle on white background",
        n=1,
        size="1024x1024",
        quality="auto",
    )
    print(f"Success! URL: {response.data[0].url}")
    print()
except Exception as e:
    print(f"Failed: {e}")
    print()
