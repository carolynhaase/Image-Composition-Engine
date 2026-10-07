from abc import ABC, abstractmethod
import numpy as np
from PIL import Image
import scipy.ndimage
from pathlib import Path




from img_comp_engine.images import array_from_file, show_from_array

class Layer:
    def __init__(self,name,filters):
          #load the image
          self.img: np.ndarray = array_from_file(name)
          self.filters: list[Filter] = filters
          self.name: str = name
          

class Filter(ABC):

    @abstractmethod
    def apply(self, img: np.ndarray) -> np.ndarray:
        ''' Applique le filtre et renvoie une image sous forme de tableau'''
        raise NotImplementedError

class BrightnessFilter(Filter):
    def __init__(self,params):
        self.level = params["level"]

    def apply(self,img :np.ndarray) -> np.ndarray:
        return np.clip(img + self.level, 0.0, 1.0)

class GrayscaleFilter(Filter):
    def apply(self,img: np.ndarray) -> np.ndarray:
        gray = (img[:,:, 0] + img[:, :, 1] + img[:, :, 2]) / 3
        new_img = np.stack((gray, gray, gray),axis = -1)
        return new_img



#layer functions

def filter_layers(layers: list[Layer], output_dir):
        output_dir = "output"
        for layer in layers:
            img = layer.img.copy()
            for filter in layer.filters:
                img= filter.apply(img)
            save_img(img, output_dir + "/" + layer.name)



          


image = array_from_file("Images/image1.jpg")

#layer list
#filter_layers([Layer("image.png",[Gaussianblur(4,3), Grayscale()])], Layer("image2.png",Sepia()))

filters = [
    GrayscaleFilter(),
    BrightnessFilter({"level": 0.4})
]


for image_filter in filters:
    image = image_filter.apply(image)

im_orig = array_from_file("Images/image1.jpg")
show_from_array(im_orig)
show_from_array(image)
