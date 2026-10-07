from pathlib import Path
import json

from img_comp_engine.layer import Layer
from img_comp_engine.images import save_img 
from img_comp_engine.filters import GaussianBlurFilter, GrayscaleFilter, BrightnessFilter, InvertFilter


def filter_layers(layers: list[Layer], output_dir):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        for layer in layers:
            img = layer.img.copy()

            for image_filter in layer.filters:
                img= image_filter.apply(img)

            save_img(img, str(output_dir / Path(layer.name).name))

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

        elif filter_config["name"] == "invert":
                    filters.append(InvertFilter())

        else:
            raise ValueError(f"Filtre non pris en charge : {filter_config['name']}")

    image_path = Path("Images") / layer_config["image"]
    layers.append(Layer(image_path, filters))

filter_layers(layers, "output")