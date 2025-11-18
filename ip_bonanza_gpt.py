#!/usr/bin/env python3
"""
IP Bonanza Image Test
Extract from: ip_bonanza.ipynb
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
Generate a photo connsisting of all the following distinct characters, all sitting at a corner stall at a popular nightclub, in order from left to right:
- Super Mario (Nintendo)
- Mickey Mouse (Disney)
- Bugs Bunny (Warner Bros)
- Pikachu (The Pokémon Company)
- Optimus Prime (Hasbro)
- Hello Kitty (Sanrio)

All of the characters MUST obey the FOLLOWING descriptions:
- The characters are having a good time
- The characters have the EXACT same physical proportions and designs consistent with their source media
- The characters have subtle facial expressions and body language consistent with that of having taken psychedelics

The composition of the image MUST obey ALL the FOLLOWING descriptions:
- The nightclub is extremely realistic, to starkly contrast with the animated depictions of the characters
  - The lighting of the nightclub is EXTREMELY dark and moody, with strobing lights
- The photo has an overhead perspective of the corner stall
- Tall cans of White Claw Hard Seltzer, bottles of Grey Goose vodka, and bottles of Jack Daniels whiskey are messily present on the table, among other brands of liquor
  - All brand logos are highly visible
  - Some characters are drinking the liquor
- The photo is low-light, low-resolution, and taken with a cheap smartphone camera
"""

    print("Generating: IP Bonanza (Characters at nightclub)...")

    generate_multiple_images(
        client=client,
        prompt=prompt,
        base_name="ip_bonanza_characters_nightclub",
        output_dir=output_dir,
        count=5,
    )

    print("\nDone!")


if __name__ == "__main__":
    main()
