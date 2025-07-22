"""
Utility functions for AI Image Caption Generator (Streamlit app)
"""

from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import io

# Function to load the BLIP model and processor
# You can optionally cache this in the app using st.cache_resource

def load_model(model_name="Salesforce/blip-image-captioning-base"):
    """Load the BLIP processor and model."""
    processor = BlipProcessor.from_pretrained(model_name)
    model = BlipForConditionalGeneration.from_pretrained(model_name)
    return processor, model


def generate_caption(image_bytes, max_length, processor=None, model=None):
    """
    Generate a caption for an image using BLIP.
    Args:
        image_bytes (bytes): Image data in bytes (e.g., from file upload)
        max_length (int): Maximum length of the generated caption
        processor: BLIP processor (optional, will load if None)
        model: BLIP model (optional, will load if None)
    Returns:
        str: Generated caption
    """
    if processor is None or model is None:
        processor, model = load_model()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    inputs = processor(image, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_length=max_length,
            min_length=max(5, max_length // 2),  # Encourage longer captions
            num_beams=5,
            early_stopping=True,
            no_repeat_ngram_size=2
        )
    caption = processor.decode(output[0], skip_special_tokens=True)
    return caption


def get_image_details(image):
    """
    Extract details from a PIL Image for display.
    Args:
        image (PIL.Image): The image object
    Returns:
        dict: Details (size, format, mode)
    """
    return {
        "size": image.size,
        "width": image.size[0],
        "height": image.size[1],
        "format": image.format,
        "mode": image.mode
    }