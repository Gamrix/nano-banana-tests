#!/usr/bin/env python3
"""
Character JSON Image Tests
Extract from: character_json.ipynb
"""

import json

from image_gen_helper import (
    ensure_output_dir,
    generate_multiple_images,
    get_openai_client,
)


def main():
    # Initialize
    client = get_openai_client()
    output_dir = ensure_output_dir()

    # Load the character JSON
    with open("paladin_pirate_barista.json", "r") as f:
        char_json = json.load(f)

    char_json_str = json.dumps(char_json, indent=2)

    # Prompt 1: Basic Vanity Fair cover
    prompt1 = f"""
Generate a photo featuring the specified person. The photo is taken for a Vanity Fair cover profile of the person. Do not include any logos, text, or watermarks.
---
{char_json_str}
"""

    print("Generating: Character JSON Attempt #1 (Basic Vanity Fair cover)...")
    generate_multiple_images(
        client=client,
        prompt=prompt1,
        base_name="character_json_attempt1_basic",
        output_dir=output_dir,
        count=5,
    )

    print()

    # Prompt 2: Detailed with camera specs
    prompt2 = f"""
Generate a photo featuring a closeup of the specified human person. The person is standing rotated 20 degrees making their `signature_pose` and their complete body is visible in the photo at the `nationality_origin` location. The photo is taken with a Canon EOS 90D DSLR camera for a Vanity Fair cover profile of the person with real-world natural lighting and real-world natural uniform depth of field (DOF). Do not include any logos, text, or watermarks.

The photo MUST accurately include and display all of the person's attributes from this JSON:
---
{char_json_str}
"""

    print("Generating: Character JSON Attempt #2 (Detailed with camera specs)...")
    generate_multiple_images(
        client=client,
        prompt=prompt2,
        base_name="character_json_attempt2_detailed",
        output_dir=output_dir,
        count=5,
    )

    print("\nDone!")


if __name__ == "__main__":
    main()
