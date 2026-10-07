from typing import Any
from PIL import Image
import numpy as np
from pathlib import Path
from abc import ABC, abstractmethod
import scipy.ndimage

from img_comp_engine.filters import Layer, save_img, show_from_array, array_from_file

class Blend(ABC):
    @abstractmethod
    def apply(self, background:np.ndarray, image: np.ndarray, opacity: float):
        raise NotImplementedError

class DifferenceBlend(Blend):
    def apply(self, background: np.ndarray, image: np.ndarray, opacity: float) -> np.ndarray:
        return background - opacity *image

"""def blend_layers(background: np.ndarray, image: np.ndarray, opacity: float, output_dir: str | Path, layer: Layer) -> np.ndarray:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        img = DifferenceBlend().apply(background, image, opacity)
        return img
        save_img(img, str(output_dir / f"blend{layer.name}.png"))

blend_layers([Layer("0_photo.jpg",,1), Layer("1_pop_bike.png",,.32),1])"""
img_dir = Path(__file__).parent / "Images"
img = DifferenceBlend().apply(array_from_file(img_dir /"0_photo.jpg"), array_from_file(img_dir / "1_pop_bike.png"), .75)
show_from_array(img)
input("hey")

