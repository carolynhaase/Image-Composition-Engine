from abc import ABC, abstractmethod
import numpy as np
from pathlib import Path
import json
from scipy.signal import convolve2d


from img_comp_engine.layer import Layer
from img_comp_engine.images import save_img
         

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



class GaussianBlurFilter(Filter):
    def __init__(self, params):
        self.window = params["window"]
        self.sigma = params["sigma"]

        if type(self.window) is not int or self.window <= 0 or self.window % 2 == 0:
            raise ValueError("window doit être un entier positif impair")

        if self.sigma <= 0:
            raise ValueError("sigma doit être strictement positif")

    def apply(self, img: np.ndarray) -> np.ndarray:
        radius = self.window // 2
        coordinates = np.arange(-radius, radius + 1)
        x, y = np.meshgrid(coordinates, coordinates)

        kernel = np.exp(-(x**2 + y**2) / (2 * self.sigma**2))
        kernel /= kernel.sum()

        channels = [
            convolve2d(
                img[:, :, channel],
                kernel,
                mode="same",
                boundary="symm",
            )
            for channel in range(img.shape[2])
        ]

        return np.stack(channels, axis=-1).astype(img.dtype, copy=False)


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

        elif filter_config["name"] == "gaussianblur":
            filters.append(GaussianBlurFilter(filter_config["params"]))

        else:
            raise ValueError(f"Filtre non pris en charge : {filter_config['name']}")

    image_path = Path("Images") / layer_config["image"]
    layers.append(Layer(image_path, filters))

filter_layers(layers, "output")




