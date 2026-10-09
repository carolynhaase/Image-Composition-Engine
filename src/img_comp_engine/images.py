from pathlib import Path

import numpy as np
from PIL import Image


def array_from_file(path: str | Path) -> np.ndarray:
    '''Loads an image and returns it as an RGB array with values between 0 and 1.'''
    with Image.open(path) as image:
        return np.asarray(image.convert("RGB"), dtype=np.float32) / 255.0

def array_to_img(arr: np.ndarray) -> Image.Image:
    '''Converts an array of values between 0 and 1 into a Pillow image.'''
    adjusted = np.array(np.clip(arr, 0, 1) * 255, dtype=np.uint8)
    return Image.fromarray(adjusted)


def show_from_array(arr: np.ndarray) -> None:
    '''Displays an array as an image.'''
    array_to_img(arr).show()


def save_img(img: np.ndarray, outname: str) -> None:
    '''Saves an array of values between 0 and 1 as an image.'''
    array_to_img(img).save(outname)


    