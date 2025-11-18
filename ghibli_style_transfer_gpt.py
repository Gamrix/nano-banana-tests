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
    generate_with_image_input,
    get_openai_client,
)


def main():
    # Original prompt from notebook (verbatim)
    prompt = "Make me into Studio Ghibli."

    # Check if input image exists
    input_image_path = Path("input_images/selfie.jpg")
    if not input_image_path.exists():
        # Try alternative paths
        alternative_paths = [
            Path("input_images/selfie.png"),
            Path("selfie.jpg"),
            Path("selfie.png"),
        ]
        for alt_path in alternative_paths:
            if alt_path.exists():
                input_image_path = alt_path
                break
        else:
            print("=" * 80)
            print("No input image found!")
            print("Please place your selfie image at one of these locations:")
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

    # Generate the image
    output_path = output_dir / "ghibli_style_transfer.png"

    print("Generating Studio Ghibli style image...")
    try:
        generate_with_image_input(
            client=client,
            prompt=prompt,
            input_images=[input_image_path],
            output_path=output_path,
            model="gpt-4o",
            quality="high",
            input_fidelity="high",  # High fidelity to preserve face details
        )
        print(f"Image saved to: {output_path}")
    except Exception as e:
        print(f"Error generating image: {e}")


if __name__ == "__main__":
    main()
