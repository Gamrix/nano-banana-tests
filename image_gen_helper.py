"""
Helper functions for OpenAI image generation with gpt-image-1

gpt-image-1 is OpenAI's most advanced image generation model that supports:
- Text-to-image generation
- Image editing with input images (via Responses API or Image API)
- Multi-turn conversations
- High input fidelity for preserving details
- Transparent backgrounds
"""

import base64
import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional, Union

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()


def get_openai_client() -> OpenAI:
    """Initialize and return an OpenAI client."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found in environment or .env file. "
            "Please add OPENAI_API_KEY=your-key-here to your .env file."
        )
    return OpenAI(api_key=api_key)


def ensure_output_dir(output_dir: str = "generated_imgs_gpt") -> Path:
    """Create and return the output directory path."""
    dir_path = Path(output_dir)
    dir_path.mkdir(exist_ok=True)
    return dir_path


def encode_image_to_base64(image_path: Union[str, Path]) -> str:
    """
    Encode an image file to base64 string.

    Args:
        image_path: Path to the image file

    Returns:
        Base64-encoded string of the image
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def generate_and_save_image(
    client: OpenAI,
    prompt: str,
    output_path: Path,
    size: str = "1024x1024",
    model: str = "gpt-image-1",
    quality: str = "auto",
    background: str = "auto",
    max_retries: int = 2,
) -> str:
    """
    Generate a single image and save it to the specified path using the Image API.

    Args:
        client: OpenAI client instance
        prompt: Text prompt for image generation
        output_path: Path where the image should be saved
        size: Image size (default: "1024x1024")
        model: Model to use (default: "gpt-image-1")
        quality: Image quality - "low", "medium", "high", or "auto" (default: "auto")
        background: Background type - "transparent", "opaque", or "auto" (default: "auto")
        max_retries: Maximum number of retries on failure (default: 2)

    Returns:
        The URL or base64 data of the generated image
    """
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            # Build params - only include quality/background if model supports them
            params = {
                "model": model,
                "prompt": prompt,
                "n": 1,
                "size": size,
            }

            # gpt-image-1 supports these params, dall-e models might not
            if model == "gpt-image-1":
                params["quality"] = quality
                params["background"] = background

            response = client.images.generate(**params)

            # gpt-image-1 returns base64 data, dall-e returns URLs
            if response.data[0].b64_json:
                # Decode and save base64 image
                image_data = base64.b64decode(response.data[0].b64_json)
                with open(output_path, "wb") as f:
                    f.write(image_data)
                return "base64_data_saved"
            elif response.data[0].url:
                # Download from URL
                image_url = response.data[0].url
                urllib.request.urlretrieve(image_url, output_path)
                return image_url
            else:
                raise ValueError("API returned neither URL nor base64 data")

        except Exception as ex:
            last_error = ex
            if attempt < max_retries:
                print(f"  Attempt {attempt + 1} failed, retrying...")
            continue

    # All retries exhausted
    print(f"  ERROR: Failed to generate image after {max_retries + 1} attempts: {last_error}")
    raise last_error


def generate_multiple_images(
    client: OpenAI,
    prompt: str,
    base_name: str,
    output_dir: Path,
    count: int = 5,
    size: str = "1024x1024",
    model: str = "gpt-image-1",
    quality: str = "auto",
    background: str = "auto",
    verbose: bool = True,
    max_workers: int = 5,
) -> list[str]:
    """
    Generate multiple images from the same prompt in parallel.

    Args:
        client: OpenAI client instance
        prompt: Text prompt for image generation
        base_name: Base name for output files (will be appended with _1, _2, etc.)
        output_dir: Directory where images should be saved
        count: Number of images to generate (default: 5)
        size: Image size (default: "1024x1024")
        model: Model to use (default: "gpt-image-1")
        quality: Image quality - "low", "medium", "high", or "auto" (default: "auto")
        background: Background type - "transparent", "opaque", or "auto" (default: "auto")
        verbose: Whether to print progress information (default: True)
        max_workers: Maximum number of parallel workers (default: 5)

    Returns:
        List of URLs for all generated images
    """
    if verbose:
        print(f"  Generating {count} images in parallel...")

    def generate_single(index: int) -> tuple[int, str | None]:
        """Helper function to generate a single image"""
        output_path = output_dir / f"{base_name}_{index}.png"
        try:
            result = generate_and_save_image(
                client, prompt, output_path, size, model, quality, background
            )
            if verbose:
                print(f"  ✓ Image {index}/{count} completed")
            return (index, result)
        except Exception:
            if verbose:
                print(f"  ✗ Image {index}/{count} failed after retries")
            return (index, None)

    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = {executor.submit(generate_single, i): i for i in range(1, count + 1)}

        # Collect results as they complete
        for future in as_completed(futures):
            index, result = future.result()
            if result:
                results[index] = result

    # Return results in order
    return [results[i] for i in range(1, count + 1) if i in results]


def generate_from_prompt_list(
    client: OpenAI,
    prompts: list[dict[str, str]],
    output_dir: Path,
    count_per_prompt: int = 5,
    size: str = "1024x1024",
    model: str = "gpt-image-1",
    quality: str = "auto",
    background: str = "auto",
) -> dict[str, list[str]]:
    """
    Generate multiple images for each prompt in a list.

    Args:
        client: OpenAI client instance
        prompts: List of dicts with 'name' and 'prompt' keys
        output_dir: Directory where images should be saved
        count_per_prompt: Number of images to generate per prompt (default: 5)
        size: Image size (default: "1024x1024")
        model: Model to use (default: "gpt-image-1")
        quality: Image quality - "low", "medium", "high", or "auto" (default: "auto")
        background: Background type - "transparent", "opaque", or "auto" (default: "auto")

    Returns:
        Dictionary mapping prompt names to lists of image URLs
    """
    all_urls = {}

    for item in prompts:
        name = item["name"]
        prompt = item["prompt"]

        print(f"Generating: {name}...")

        urls = generate_multiple_images(
            client=client,
            prompt=prompt,
            base_name=name,
            output_dir=output_dir,
            count=count_per_prompt,
            size=size,
            model=model,
            quality=quality,
            background=background,
            verbose=True,
        )

        all_urls[name] = urls
        print()

    return all_urls


def generate_with_image_input(
    client: OpenAI,
    prompt: str,
    input_images: list[Union[str, Path]],
    output_path: Path,
    model: str = "gpt-4o",
    quality: str = "auto",
    input_fidelity: str = "low",
    background: str = "auto",
    size: str = "auto",
) -> str:
    """
    Generate an image using input images as references via the Responses API.

    This function uses the Responses API which allows image inputs for editing
    or using images as references for generation.

    Args:
        client: OpenAI client instance
        prompt: Text prompt for image generation/editing
        input_images: List of paths to input images (up to 4 recommended)
        output_path: Path where the generated image should be saved
        model: Model to use (e.g., "gpt-4o", "gpt-4.1", "gpt-5") (default: "gpt-4o")
        quality: Image quality - "low", "medium", "high", or "auto" (default: "auto")
        input_fidelity: Input fidelity - "low" or "high" (default: "low")
        background: Background type - "transparent", "opaque", or "auto" (default: "auto")
        size: Image size like "1024x1024" or "auto" (default: "auto")

    Returns:
        Base64-encoded image data
    """
    # Prepare input content with text and images
    content = [{"type": "input_text", "text": prompt}]

    # Add input images as base64-encoded data URLs
    for img_path in input_images:
        base64_image = encode_image_to_base64(img_path)
        content.append({
            "type": "input_image",
            "image_url": f"data:image/jpeg;base64,{base64_image}",
        })

    # Create the request
    response = client.responses.create(
        model=model,
        input=[{"role": "user", "content": content}],
        tools=[{
            "type": "image_generation",
            "quality": quality,
            "input_fidelity": input_fidelity,
            "background": background,
            "size": size,
        }],
    )

    # Extract the generated image
    image_data = None
    for output in response.output:
        if output.type == "image_generation_call" and output.status == "completed":
            image_data = output.result
            break

    if not image_data:
        raise ValueError("No image was generated")

    # Save the image
    image_buffer = base64.b64decode(image_data)
    with open(output_path, "wb") as f:
        f.write(image_buffer)

    return image_data


def generate_multiple_with_image_input(
    client: OpenAI,
    prompt: str,
    input_images: list[Union[str, Path]],
    base_name: str,
    output_dir: Path,
    count: int = 5,
    model: str = "gpt-4o",
    quality: str = "auto",
    input_fidelity: str = "low",
    background: str = "auto",
    size: str = "auto",
    verbose: bool = True,
) -> list[str]:
    """
    Generate multiple images using input images as references.

    Args:
        client: OpenAI client instance
        prompt: Text prompt for image generation/editing
        input_images: List of paths to input images
        base_name: Base name for output files (will be appended with _1, _2, etc.)
        output_dir: Directory where images should be saved
        count: Number of images to generate (default: 5)
        model: Model to use (e.g., "gpt-4o", "gpt-4.1", "gpt-5") (default: "gpt-4o")
        quality: Image quality - "low", "medium", "high", or "auto" (default: "auto")
        input_fidelity: Input fidelity - "low" or "high" (default: "low")
        background: Background type - "transparent", "opaque", or "auto" (default: "auto")
        size: Image size like "1024x1024" or "auto" (default: "auto")
        verbose: Whether to print progress information (default: True)

    Returns:
        List of base64-encoded image data
    """
    results = []

    for i in range(1, count + 1):
        if verbose:
            print(f"  Generating image {i}/{count}...")

        output_path = output_dir / f"{base_name}_{i}.png"

        try:
            image_data = generate_with_image_input(
                client=client,
                prompt=prompt,
                input_images=input_images,
                output_path=output_path,
                model=model,
                quality=quality,
                input_fidelity=input_fidelity,
                background=background,
                size=size,
            )

            if verbose:
                print(f"  Saved to: {output_path}")

            results.append(image_data)
        except Exception as e:
            print(f"  Failed to generate image {i}/{count}: {e}")
            continue

    return results
