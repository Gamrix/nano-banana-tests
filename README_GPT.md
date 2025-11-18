# OpenAI GPT Image Generation Tests

This repository contains Python scripts that extract prompts from Jupyter notebooks and generate images using OpenAI's `gpt-image-1` model.

**gpt-image-1** is OpenAI's most advanced image generation model that supports:
- Text-to-image generation via the Image API
- Image editing with input images via the Responses API
- Multi-turn conversations for iterative editing
- High input fidelity for preserving details from reference images
- Transparent backgrounds

## Setup

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- OpenAI API key

### Installation

1. Install dependencies using uv:

```bash
uv sync
```

2. Create a `.env` file from the example:

```bash
cp .env.example .env
```

3. Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your-actual-api-key-here
```

Get your API key from: https://platform.openai.com/api-keys

## Usage

All scripts generate 5 images per prompt and save them to the `generated_imgs_gpt/` directory.

### Run Individual Scripts

```bash
# Code generation (Fibonacci with refrigerator magnets)
uv run python code_generation_gpt.py

# Character JSON (Vanity Fair cover with character description)
uv run python character_json_gpt.py

# IP Bonanza (Characters at nightclub)
uv run python ip_bonanza_gpt.py

# System Prompt (Multiple refrigerator magnet prompts)
uv run python system_prompt_gpt.py

# Ghibli Style Transfer (requires input image)
uv run python ghibli_style_transfer_gpt.py

# Ugly Sonic (requires input images)
uv run python ugly_sonic_gpt.py
```

### Run All Working Scripts

```bash
uv run python code_generation_gpt.py && \
uv run python character_json_gpt.py && \
uv run python ip_bonanza_gpt.py && \
uv run python system_prompt_gpt.py
```

## Scripts Overview

### Text-Only Generation Scripts

| Script | Source Notebook | Description | Images Generated |
|--------|----------------|-------------|------------------|
| `code_generation_gpt.py` | `code_generation.ipynb` | Fibonacci code with refrigerator magnets | 5 |
| `character_json_gpt.py` | `character_json.ipynb` | Character portraits from JSON description (2 prompts) | 10 |
| `ip_bonanza_gpt.py` | `ip_bonanza.ipynb` | Cartoon characters at nightclub | 5 |
| `system_prompt_gpt.py` | `system_prompt.ipynb` | System prompt text with refrigerator magnets (5 prompts) | 25 |

**Total: 45 images**

### Image-to-Image Generation Scripts

These scripts use the Responses API to generate images based on input images:

| Script | Source Notebook | Description | Input Required |
|--------|----------------|-------------|----------------|
| `ghibli_style_transfer_gpt.py` | `ghibli_style_transfer.ipynb` | Apply Studio Ghibli style to selfie | Place selfie at `input_images/selfie.jpg` |
| `ugly_sonic_gpt.py` | `ugly_sonic.ipynb` | Generate Ugly Sonic with Obama (3 prompts, 5 each) | Place Ugly Sonic refs at `input_images/ugly_sonic_*.jpg` |

## Output Structure

All generated images are saved to `generated_imgs_gpt/` with descriptive names:

```
generated_imgs_gpt/
├── code_generation_fibonacci_magnets_1.png
├── code_generation_fibonacci_magnets_2.png
├── ...
├── character_json_attempt1_basic_1.png
├── character_json_attempt2_detailed_1.png
├── ...
├── ip_bonanza_characters_nightclub_1.png
├── ...
└── system_prompt_all_previous_text_1.png
```

## Helper Module

The `image_gen_helper.py` module provides shared utility functions:

### Basic Functions
- `get_openai_client()` - Initialize OpenAI client with API key from .env
- `ensure_output_dir()` - Create output directory if it doesn't exist
- `encode_image_to_base64()` - Encode image file to base64 string

### Text-to-Image Generation (Image API)
- `generate_and_save_image()` - Generate single image from text
- `generate_multiple_images()` - Generate multiple images from one prompt
- `generate_from_prompt_list()` - Generate images from a list of prompts

### Image-to-Image Generation (Responses API)
- `generate_with_image_input()` - Generate/edit image using input images
- `generate_multiple_with_image_input()` - Generate multiple images using input images

## Cost Estimation

Image generation with `gpt-image-1` uses token-based pricing (as of 2025):

### Text-to-Image Scripts
- Standard quality 1024x1024: ~272 image tokens (~$0.01 per image)
- Total for text-only scripts: 45 images × ~$0.01 = ~$0.45

### Image-to-Image Scripts
- Uses Responses API with mainline models (gpt-4o, gpt-4.1, gpt-5)
- Cost includes: input text tokens + input image tokens + output image tokens
- High quality with high input fidelity: ~6,240 image tokens per generation
- Variable cost depending on quality settings and number of input images

See [OpenAI pricing](https://openai.com/api/pricing/) for current rates.

## Notes

- All prompts are extracted verbatim from the original Jupyter notebooks
- Images are generated at 1024x1024 resolution
- Generation may take several minutes depending on OpenAI API response time
- Failed generations will print error messages but won't stop the script

## Troubleshooting

### "OPENAI_API_KEY not found"

Make sure you've created a `.env` file with your API key.

### "Module 'openai' not found"

Run `uv sync` to install dependencies.

### Rate Limiting

If you hit rate limits, the script will fail. Wait a few minutes and try again, or reduce the number of images generated per prompt in the script.
