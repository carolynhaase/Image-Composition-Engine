import numpy as np

from img_comp_engine.images import array_from_file
from img_comp_engine.filters import Filter

class Layer:
    def __init__(self,name,filters,opacity):
          #load the image
          self.img: np.ndarray = array_from_file(name)
          self.filters: list[Filter] = filters
          self.name: str = name
          self.opacity: float = opacity