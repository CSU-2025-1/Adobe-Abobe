from PIL import Image, ImageEnhance, ImageFilter


def apply_filters(image_path: str, filters: dict) -> str:
    image = Image.open(image_path).convert("RGB")

    brightness = filters.get("brightness", 1.0)
    contrast = filters.get("contrast", 1.0)
    blur = filters.get("blur", 0.0)

    image = ImageEnhance.Brightness(image).enhance(brightness)
    image = ImageEnhance.Contrast(image).enhance(contrast)

    if blur > 0.0:
        image = image.filter(ImageFilter.GaussianBlur(radius=blur))

    output_path = image_path.replace(".jpg", "_filtered.jpg")
    image.save(output_path, format="JPEG")

    return output_path
