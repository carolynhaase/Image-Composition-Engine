from pathlib import Path
import json

from img_comp_engine.layer import Layer
from img_comp_engine.images import save_img 
from img_comp_engine.blend import blend_layers
from img_comp_engine.filters import GaussianBlurFilter, GrayscaleFilter, BrightnessFilter, InvertFilter, ContrastFilter


def filter_layers(layers: list[Layer], output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    composition = None

    for layer in layers:
        img = layer.img.copy()

        for image_filter in layer.filters:
            img = image_filter.apply(img)

        if composition is None:
            composition = img
        else:
            if img.shape != composition.shape:
                expected_height, expected_width = composition.shape[:2]
                actual_height, actual_width = img.shape[:2]

                raise ValueError(
                    f"Dimensions incompatibles pour la couche "
                    f"'{Path(layer.name).name}'"
                )

            composition = blend_layers(composition, img, layer.opacity, layer.blend)

    if composition is None:
        raise ValueError("La configuration ne contient aucune couche à composer.")

    save_img(composition, str(output_dir / "composition.png"))



def run(config_path: str | Path, images_dir: str | Path, output_dir: str | Path) -> None:
    config_path = Path(config_path)
    images_dir = Path(images_dir)

    with config_path.open(encoding="utf-8") as file:
        config = json.load(file)

    layers = []

    for layer_config in config["layers"]:
        filters = []

        for filter_config in layer_config["filters"]:
            name = filter_config["name"]
            params = filter_config.get("params", {})

            if name == "grayscale":
                filters.append(GrayscaleFilter())
            elif name == "brightness":
                filters.append(BrightnessFilter(params))
            elif name == "gaussianblur":
                filters.append(GaussianBlurFilter(params))
            elif name == "invert":
                filters.append(InvertFilter())
            elif name == "contrast":
                filters.append(ContrastFilter(params))
            else:
                raise ValueError(f"Filtre non pris en charge : {name}")

        image_path = images_dir / layer_config["image"]
        layers.append(Layer(image_path, filters, layer_config.get("opacity", 1.0), layer_config.get("blend", "normal"))
)

    filter_layers(layers, output_dir)