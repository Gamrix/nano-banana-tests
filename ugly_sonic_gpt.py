#!/usr/bin/env python3
"""
Ugly Sonic Image Tests
Extract from: ugly_sonic.ipynb

This script uses OpenAI's Responses API with image inputs to create images of
Ugly Sonic with Barack Obama, using reference images of Ugly Sonic.
"""

from pathlib import Path

from image_gen_helper import (
    ensure_output_dir,
    generate_multiple_with_image_input,
    get_openai_client,
)


def main():
    # Original prompts from notebook (verbatim)
    prompts = [
        {
            "name": "ugly_sonic_obama_basic",
            "prompt": "Create an image of the character in all the user-provided images smiling with their mouth open while shaking hands with President Barack Obama.",
        },
        {
            "name": "ugly_sonic_obama_pulitzer",
            "prompt": "Create an image of the character in all the user-provided images smiling with their mouth open while shaking hands with President Barack Obama. Pulitzer-prize-winning cover photo for the The New York Times.",
        },
        {
            "name": "ugly_sonic_obama_no_watermarks",
            "prompt": "Create an image of the character in all the user-provided images smiling with their mouth open while shaking hands with President Barack Obama. Pulitzer-prize-winning cover photo for the The New York Times. Do not include any text or watermarks.",
        },
    ]

    # Check for input images of Ugly Sonic in multiple locations
    ugly_sonic_images = []

    # Try prompt_imgs first
    prompt_imgs_dir = Path("prompt_imgs")
    if prompt_imgs_dir.exists():
        ugly_sonic_images.extend(list(prompt_imgs_dir.glob("ugly_sonic*.jpg")))
        ugly_sonic_images.extend(list(prompt_imgs_dir.glob("ugly_sonic*.png")))
        ugly_sonic_images.extend(list(prompt_imgs_dir.glob("ugly_sonic*.webp")))

    # Try input_images as fallback
    if not ugly_sonic_images:
        input_dir = Path("input_images")
        if input_dir.exists():
            ugly_sonic_images.extend(list(input_dir.glob("ugly_sonic*.jpg")))
            ugly_sonic_images.extend(list(input_dir.glob("ugly_sonic*.png")))
            ugly_sonic_images.extend(list(input_dir.glob("ugly_sonic*.webp")))

    if not ugly_sonic_images:
        print("=" * 80)
        print("No Ugly Sonic reference images found!")
        print("Please place Ugly Sonic reference images at:")
        print("  - prompt_imgs/ugly_sonic_1.webp")
        print("  - prompt_imgs/ugly_sonic_2.webp")
        print("  - input_images/ugly_sonic_1.jpg")
        print("  - input_images/ugly_sonic_2.jpg")
        print("  - etc.")
        print()
        print("You can use multiple reference images for better character consistency.")
        print("=" * 80)
        return

    print("=" * 80)
    print("Ugly Sonic Image Generation")
    print("=" * 80)
    print(f"Found {len(ugly_sonic_images)} reference image(s):")
    for img in ugly_sonic_images:
        print(f"  - {img}")
    print()

    # Initialize client and output directory
    client = get_openai_client()
    output_dir = ensure_output_dir("generated_imgs_gpt")

    # Generate images for each prompt
    for item in prompts:
        name = item["name"]
        prompt = item["prompt"]

        print(f"Generating: {name}...")
        print(f"Prompt: {prompt}")
        print()

        try:
            generate_multiple_with_image_input(
                client=client,
                prompt=prompt,
                input_images=ugly_sonic_images,
                base_name=name,
                output_dir=output_dir,
                count=5,
                model="gpt-5",
                quality="high",
                input_fidelity="high",  # High fidelity to preserve character details
            )
            print()
        except Exception as e:
            print(f"Error generating images for {name}: {e}")
            print()


if __name__ == "__main__":
    main()
