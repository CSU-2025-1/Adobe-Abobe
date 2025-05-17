from PIL import Image, ImageEnhance, ImageFilter
import os
import numpy as np

from utils.filters_registry import register_filter
from utils.filters_registry import FILTER_REGISTRY


def _apply_filter(image_path: str, filter_config: dict) -> str:
    image = Image.open(image_path).convert("RGB")
    filter_type = filter_config.get("type")
    value = filter_config.get("value")

    if filter_type not in FILTER_REGISTRY:
        raise ValueError(f"Unsupported filter type: {filter_type}")

    filtered_image = FILTER_REGISTRY[filter_type](image, value)

    base, ext = os.path.splitext(image_path)
    output_path = f"{base}_{filter_type}_{str(value).replace('.', '_')}.jpg"
    filtered_image.save(output_path, format="JPEG")
    return output_path


@register_filter("brightness")
def apply_brightness(image, value):
    return ImageEnhance.Brightness(image).enhance(value)


@register_filter("contrast")
def apply_contrast(image, value):
    return ImageEnhance.Contrast(image).enhance(value)


@register_filter("sharpness")
def apply_sharpness(image, value):
    return ImageEnhance.Sharpness(image).enhance(value)


@register_filter("color")
def apply_color(image, value):
    return ImageEnhance.Color(image).enhance(value)


@register_filter("blur")
def apply_blur(image, value):
    if value > 0:
        return image.filter(ImageFilter.GaussianBlur(radius=value))
    return image


@register_filter("gamma")
def apply_gamma(image, value):
    inv_gamma = 1.0 / value
    table = [min(255, int((i / 255.0) ** inv_gamma * 255)) for i in range(256)]
    return image.point(table * 3)


@register_filter("sepia")
def apply_sepia(image, value):
    img = np.array(image).astype(np.float32)
    r, g, b = img[..., 0], img[..., 1], img[..., 2]
    sepia = np.stack([
        r * 0.393 + g * 0.769 + b * 0.189,
        r * 0.349 + g * 0.686 + b * 0.168,
        r * 0.272 + g * 0.534 + b * 0.131
    ], axis=-1)
    result = (sepia * value + img * (1 - value))
    return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))


@register_filter("temperature")
def apply_temperature(image, value):
    r_adj = int((value - 6500) / 1000 * 20)
    b_adj = -r_adj
    r, g, b = image.split()
    r = r.point(lambda i: min(255, max(0, i + r_adj)))
    b = b.point(lambda i: min(255, max(0, i + b_adj)))
    return Image.merge("RGB", (r, g, b))


@register_filter("exposure")
def apply_exposure(image, value):
    factor = 1 + value
    image = ImageEnhance.Brightness(image).enhance(factor)
    image = ImageEnhance.Contrast(image).enhance(factor)
    return image


@register_filter("hue")
def apply_hue(image, value):
    import colorsys
    img = np.array(image).astype(np.float32) / 255.0
    r, g, b = img[..., 0], img[..., 1], img[..., 2]
    hls = np.vectorize(colorsys.rgb_to_hls)(r, g, b)
    h = (hls[0] + value / 360.0) % 1.0
    rgb = np.vectorize(colorsys.hls_to_rgb)(h, hls[1], hls[2])
    result = np.stack(rgb, axis=-1)
    return Image.fromarray((np.clip(result, 0, 1) * 255).astype(np.uint8))
