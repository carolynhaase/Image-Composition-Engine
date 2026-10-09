import numpy as np
from abc import ABC, abstractmethod


class Blend(ABC):
    @abstractmethod
    def apply(self, background:np.ndarray, image: np.ndarray, opacity: float)-> np.ndarray :
        raise NotImplementedError

class NormalBlend(Blend):
    # Puts the image over the background, according to the opacity
    def apply(self, background: np.ndarray, image: np.ndarray,opacity:float) -> np.ndarray:
        return background *(1-opacity)+image*opacity
    
class DifferenceBlend(Blend):
    # Takes the absolute difference between background and image
    def apply(self, background: np.ndarray, image: np.ndarray, opacity: float) -> np.ndarray:
        difference = np.abs(background - image)
        return background * (1-opacity) + difference * opacity

class MultiplyBlend(Blend):
    # Multiplies background and image pixel by pixel (darkens)
    def apply(self, background: np.ndarray, image: np.ndarray, opacity: float) -> np.ndarray:
        multiplied = background * image
        return background * (1 - opacity) + multiplied * opacity

class LightenBlend(Blend):
     # Keeps the lighter of the two pixels, pixel by pixel
     def apply(self, background: np.ndarray, image: np.ndarray, opacity: float) -> np.ndarray:
        lightened = np.maximum(background, image)
        return background * (1 - opacity) + lightened * opacity
          





