from typing import Any

import numpy as np
from abc import ABC, abstractmethod

class Blend(ABC):
    @abstractmethod
    def apply(self, background:np.ndarray, image: np.ndarray, opacity: float):
        raise NotImplementedError

class DifferenceBlend(Blend):
    def apply(self, background: np.ndarray, image: np.ndarray, opacity: float) -> np.ndarray:
        return background - opacity *image
