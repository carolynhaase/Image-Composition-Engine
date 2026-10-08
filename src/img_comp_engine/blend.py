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
    def apply(self, background:np.ndarray, image: np.ndarray, opacity: float)-> np.ndarray :
        raise NotImplementedError

class NormalBlend(Blend):
    #display the image over the background (no opacity)
    #same as using DifferenceBlend with 100% opacity
    def apply(self, background: np.ndarray, image: np.ndarray,opacity:float) -> np.ndarray:
        return background *(1-opacity)+image*opacity
    
class DifferenceBlend(Blend):
    #display the image with specific opacity over the background
    def apply(self, background: np.ndarray, image: np.ndarray, opacity: float) -> np.ndarray:
        difference = np.abs(background - image)
        return background * (1-opacity) + difference * opacity

class MultiplyBlend(Blend):
    def apply(self, background: np.ndarray, image: np.ndarray, opacity: float) -> np.ndarray:
        multiplied = background * image
        return background * (1 - opacity) + multiplied * opacity

class LightenBlend(Blend):
     def apply(self, background: np.ndarray, image: np.ndarray, opacity: float) -> np.ndarray:
        lightened = np.maximum(background, image)
        return background * (1 - opacity) + lightened * opacity
          
    
"""
def blend_layers(background: np.ndarray, image: np.ndarray, opacity: float, output_dir: str | Path) -> np.ndarray:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        img = DifferenceBlend().apply(background, image, opacity)
        return img
        #save_img(img, str(output_dir / f"blend{layer.name}.png"))
"""

def blend_layers(background: np.ndarray, image: np.ndarray, opacity:float, blend_mode: str = "normal") -> np.ndarray:
        if blend_mode == "normal":
             blend = NormalBlend()
        elif blend_mode == "difference":
             blend = DifferenceBlend()
        elif blend_mode == "multiply":
             blend = MultiplyBlend()
        elif blend_mode == "lighten":
             blend = LightenBlend()
        else:
             raise ValueError(f"Mode de mélange non pris en charge :{blend_mode}")
        
        return blend.apply(background,image,opacity)

#blend_layers([Layer("0_photo.jpg",(),1), Layer("1_pop_bike.png",(),.32),1])


"""
img_dir = Path(__file__).parent / "Images"
img = DifferenceBlend().apply(array_from_file(img_dir /"0_photo.jpg"), array_from_file(img_dir / "1_pop_bike.png"), .75)
show_from_array(img)
input("hey")
"""
