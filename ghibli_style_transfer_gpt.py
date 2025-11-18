#!/usr/bin/env python3
"""
Ghibli Style Transfer Image Test
Extract from: ghibli_style_transfer.ipynb

This script uses OpenAI's Responses API with image inputs to apply Studio Ghibli style
to an input image (e.g., a selfie).
"""

from pathlib import Path

from image_gen_helper import (
    ensure_output_dir,
    generate_multiple_with_image_input,
    get_openai_client,
)


def main():
    # Original prompt from notebook (verbatim)
    prompt = "Make me into Studio Ghibli."

    # Check if input image exists - try multiple locations
    possible_paths = [
        Path("prompt_imgs/max_selfie.webp"),
        Path("input_images/selfie.jpg"),
        Path("input_images/selfie.png"),
        Path("input_images/selfie.webp"),
        Path("selfie.jpg"),
        Path("selfie.png"),
    ]

    input_image_path = None
    for path in possible_paths:
        if path.exists():
            input_image_path = path
            break

    if not input_image_path:
        print("=" * 80)
        print("No input image found!")
        print("Please place your selfie image at one of these locations:")
        print("  - prompt_imgs/max_selfie.webp")
        print("  - input_images/selfie.jpg")
        print("  - input_images/selfie.png")
        print("  - selfie.jpg")
        print("  - selfie.png")
        print("=" * 80)
        return

    print("=" * 80)
    print("Ghibli Style Transfer")
    print("=" * 80)
    print(f"Input image: {input_image_path}")
    print(f"Prompt: {prompt}")
    print()

    # Initialize client and output directory
    client = get_openai_client()
    output_dir = ensure_output_dir("generated_imgs_gpt")

    print("Generating 5 Studio Ghibli style images...")
    try:
        generate_multiple_with_image_input(
            client=client,
            prompt=prompt,
            input_images=[input_image_path],
            base_name="ghibli_style_transfer",
            output_dir=output_dir,
            count=5,
            model="gpt-5",
            quality="high",
            input_fidelity="high",  # High fidelity to preserve face details
        )
        print("\nAll images saved!")
    except Exception as e:
        print(f"Error generating images: {e}")


if __name__ == "__main__":
    main()
