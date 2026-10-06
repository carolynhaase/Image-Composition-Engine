from abc import ABC, abstractmethod
import numpy as np 


from img_comp_engine.images import array_from_file, show_from_array


class Filter(ABC):

    @abstractmethod
    def apply(img: np.ndarray) -> np.ndarray:
        ''' Applique le filtre et renvoie une image sous forme de tableau'''
        raise NotImplementedError

class BrightnessFilter(Filter):
    def __init__(self,params):
        self.level = params["level"]

    def apply(self,img :np.ndarray) -> np.ndarray:
        return np.clip(img + self.level, 0.0, 1.0)


image = array_from_file("Images/image1.jpg")

filters = [
    BrightnessFilter({"level": 0.4}),
]


for image_filter in filters:
    image = image_filter.apply(image)

im_orig = array_from_file("Images/image1.jpg")
show_from_array(im_orig)
show_from_array(image)