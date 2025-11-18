#!/usr/bin/env python3
"""
Code Generation Image Test
Extract from: code_generation.ipynb
"""

from image_gen_helper import (
    ensure_output_dir,
    generate_multiple_images,
    get_openai_client,
)


def main():
    # Initialize
    client = get_openai_client()
    output_dir = ensure_output_dir()

    # Prompt from notebook
    prompt = """
Create an image depicting a minimal recursive Python implementation `fib()` of the Fibonacci sequence using many large refrigerator magnets as the letters and numbers for the code:
- The magnets are placed on top of an expensive aged wooden table.
- All code characters MUST EACH be colored according to standard Python syntax highlighting.
- All code characters MUST follow proper Python indentation and formatting.

The image is a top-down perspective taken with a Canon EOS 90D DSLR camera for a viral 4k HD MKBHD video with neutral diffuse lighting. Do not include any watermarks.
"""

    print("Generating: Code Generation (Fibonacci with refrigerator magnets)...")

    generate_multiple_images(
        client=client,
        prompt=prompt,
        base_name="code_generation_fibonacci_magnets",
        output_dir=output_dir,
        count=5,
    )

    print("\nDone!")


if __name__ == "__main__":
    main()
