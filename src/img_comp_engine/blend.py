from typing import Any
from PIL import Image
import numpy as np
from pathlib import Path
from abc import ABC, abstractmethod
import scipy.ndimage

from img_comp_engine.images import save_img, show_from_array, array_from_file
from img_comp_engine.layer import Layer

class Blend(ABC):
    @abstractmethod
    def apply(self, type: str, background:np.ndarray, image: np.ndarray, opacity: float):
        self.type: str = type
        raise NotImplementedError

class NormalBlend(Blend):
    #display the image over the background (no opacity)
    #same as using DifferenceBlend with 100% opacity
    def apply(self, background: np.ndarray, image: np.ndarray) -> np.ndarray:
        img = background.copy()
         # Find pixels where both images contain non-zero color
        overlap = np.any(background != 0, axis=-1) & np.any(image != 0, axis=-1)

        # Replace only those overlapping pixels with the foreground image
        img[overlap] = image[overlap]
        return img
    
class DifferenceBlend(Blend):
    #display the image with specific opacity over the background
    def apply(self, background: np.ndarray, image: np.ndarray, opacity: float) -> np.ndarray:
        return background - opacity *image
    
"""
def blend_layers(background: np.ndarray, image: np.ndarray, opacity: float, output_dir: str | Path) -> np.ndarray:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        img = DifferenceBlend().apply(background, image, opacity)
        return img
        #save_img(img, str(output_dir / f"blend{layer.name}.png"))
"""

def blend_layers(background: np.ndarray, image: np.ndarray, output_dir: str | Path) -> np.ndarray:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        img = NormalBlend().apply(background, image)
        return img
#blend_layers([Layer("0_photo.jpg",(),1), Layer("1_pop_bike.png",(),.32),1])
img_dir = Path(__file__).parent / "Images"
background = array_from_file(img_dir / "0_photo.jpg")
image = array_from_file(img_dir / "1_pop_bike.png")
im_blend = blend_layers(background, image, Path("output"))
show_from_array(im_blend)
input("hey")

"""
img_dir = Path(__file__).parent / "Images"
img = DifferenceBlend().apply(array_from_file(img_dir /"0_photo.jpg"), array_from_file(img_dir / "1_pop_bike.png"), .75)
show_from_array(img)
input("hey")
"""
