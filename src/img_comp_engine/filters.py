from abc import ABC, abstractmethod
import numpy as np
from PIL import Image
import scipy.ndimage
from pathlib import Path
import json




from img_comp_engine.images import array_from_file, show_from_array, save_img
from img_comp_engine.images import array_from_file, show_from_array, save_img

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
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        for layer in layers:
            img = layer.img.copy()

            for image_filter in layer.filters:
                img= image_filter.apply(img)

            save_img(img, str(output_dir / Path(layer.name).name))


          


#layer list
#filter_layers([Layer("image.png",[Gaussianblur(4,3), Grayscale()])], Layer("image2.png",Sepia()))


with open("config.json", encoding="utf-8") as file:
    config = json.load(file)

layers = []

for layer_config in config["layers"]:
    filters = []

    for filter_config in layer_config["filters"]:

        if filter_config["name"] == "grayscale":
            filters.append(GrayscaleFilter())

        elif filter_config["name"] == "brightness":
            filters.append(BrightnessFilter(filter_config["params"]))

        else:
            raise ValueError(f"Filtre non pris en charge : {filter_config['name']}")

    image_path = Path("Images") / layer_config["image"]
    layers.append(Layer(image_path, filters))

filter_layers(layers, "output")


