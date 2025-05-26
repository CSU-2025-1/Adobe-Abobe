import cv2
import numpy as np
from utils.filters_registry import register_filter


@register_filter("brightness")
def apply_brightness(image: np.ndarray, value: float) -> np.ndarray:
    return cv2.convertScaleAbs(image, alpha=value, beta=0)


@register_filter("contrast")
def apply_contrast(image: np.ndarray, value: float) -> np.ndarray:
    factor = 131 * (value + 127) / (127 * (131 - value))
    table = np.array([
        np.clip(factor * (i - 127) + 127, 0, 255) for i in range(256)
    ]).astype("uint8")
    return cv2.LUT(image, table)


@register_filter("blur")
def apply_blur(image: np.ndarray, value: float) -> np.ndarray:
    ksize = int(2 * round(value) + 1)
    return cv2.GaussianBlur(image, (ksize, ksize), 0)


@register_filter("sharpness")
def apply_sharpness(image: np.ndarray, value: float) -> np.ndarray:
    kernel = np.array([
        [0, -1, 0],
        [-1, 5 + value, -1],
        [0, -1, 0]
    ])
    return cv2.filter2D(image, -1, kernel)


@register_filter("color")
def apply_color(image: np.ndarray, value: float) -> np.ndarray:
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV).astype(np.float32)
    hsv[..., 1] *= value
    hsv[..., 1] = np.clip(hsv[..., 1], 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)


@register_filter("gamma")
def apply_gamma(image: np.ndarray, value: float) -> np.ndarray:
    inv_gamma = 1.0 / value
    table = np.array([(i / 255.0) ** inv_gamma * 255 for i in np.arange(256)]).astype("uint8")
    return cv2.LUT(image, table)


@register_filter("sepia")
def apply_sepia(image: np.ndarray, value: float) -> np.ndarray:
    sepia_kernel = np.array([[0.393, 0.769, 0.189],
                             [0.349, 0.686, 0.168],
                             [0.272, 0.534, 0.131]])
    sepia_img = image @ sepia_kernel.T
    sepia_img = np.clip(sepia_img, 0, 255).astype(np.uint8)
    return cv2.addWeighted(image, 1 - value, sepia_img, value, 0)


@register_filter("temperature")
def apply_temperature(image: np.ndarray, value: float) -> np.ndarray:
    b, g, r = cv2.split(image.astype(np.float32))
    r += (value - 6500) / 100
    b -= (value - 6500) / 100
    merged = cv2.merge([np.clip(b, 0, 255), g, np.clip(r, 0, 255)])
    return merged.astype(np.uint8)


@register_filter("exposure")
def apply_exposure(image: np.ndarray, value: float) -> np.ndarray:
    return cv2.convertScaleAbs(image, alpha=1 + value, beta=0)


@register_filter("hue")
def apply_hue(image: np.ndarray, value: float) -> np.ndarray:
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV).astype(np.float32)
    hsv[..., 0] = (hsv[..., 0] + (value / 2)) % 180
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
