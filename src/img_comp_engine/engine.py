from pathlib import Path
import json
import numpy as np

from img_comp_engine.layer import Layer
from img_comp_engine.images import save_img 

from img_comp_engine.blend import (
    NormalBlend,
    DifferenceBlend,
    MultiplyBlend,
    LightenBlend
)
from img_comp_engine.filters import (
    GaussianBlurFilter, 
    GrayscaleFilter, 
    BrightnessFilter, 
    InvertFilter,
    ContrastFilter
)

BLENDS = {
    "normal": NormalBlend,
    "difference": DifferenceBlend,
    "multiply": MultiplyBlend,
    "lighten": LightenBlend,
}
 
FILTERS = {
    "grayscale": GrayscaleFilter,
    "brightness": BrightnessFilter,
    "gaussianblur": GaussianBlurFilter,
    "invert": InvertFilter,
    "contrast": ContrastFilter,
}


def blend_layers(background: np.ndarray, image: np.ndarray, opacity: float, blend_mode: str = "normal") -> np.ndarray:
    if blend_mode not in BLENDS:
        raise ValueError(f"Unsupported blend mode : {blend_mode}")
 
    blend = BLENDS[blend_mode]()
    return blend.apply(background, image, opacity)



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
                    f"Incompatible dimensions for layer "
                    f"'{Path(layer.name).name}': expected "
                    f"{expected_width}x{expected_height}, got "
                    f"{actual_width}x{actual_height}"
                )
 
            composition = blend_layers(composition, img, layer.opacity, layer.blend)
 
    if composition is None:
        raise ValueError("The configuration contains no layers to compose.")
 
    save_img(composition, str(output_dir / "composition.png"))



def run(config_path: str | Path, images_dir: str | Path, output_dir: str | Path) -> None:
    config_path = Path(config_path)
    images_dir = Path(images_dir)
 
    with config_path.open(encoding="utf-8") as file:
        config = json.load(file)
 
    layers = []
 
    for layer_config in config["layers"]:
        filters = []
 
        for filter_config in layer_config.get("filters", []):
            name = filter_config["name"]
            params = filter_config.get("params", {})
 
            if name not in FILTERS:
                raise ValueError(f"Unsupported filter : {name}")
 
            filters.append(FILTERS[name](params))
 
        opacity = layer_config.get("opacity", 1.0)
        if not 0 <= opacity <= 1:
            raise ValueError(f"Opacity must be between 0 and 1 (got {opacity})")
 
        image_path = images_dir / layer_config["image"]
        blend = layer_config.get("blend", "normal")
        layers.append(Layer(image_path, filters, opacity, blend))
 
    filter_layers(layers, output_dir)