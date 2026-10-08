import numpy as np
from abc import ABC, abstractmethod


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
          





