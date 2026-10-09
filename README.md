# Image Composition Engine

A small Python tool that stacks several images into one, like layers in Photoshop or GIMP. Each layer can have filters (blur, contrast, invert...), an opacity and a blend mode. Everything is described in a simple YAML file, so you can change the result without touching the code.

## How it works

1. You describe your layers in `conf.yml`.
2. For each layer, the engine loads the image and applies its filters in order.
3. The layers are blended from bottom to top: the first layer is the background, and each following layer is blended onto the result so far.
4. The final image is saved as `output/composition.png`.

Images are handled as NumPy arrays of RGB values between 0 and 1.

## Installation

Dependencies: NumPy, Pillow, SciPy, PyYAML (installed by `uv sync`).

## Usage

1. Put your images in the `Images/` folder, next to `main.py`.
2. Edit `conf.yml` (see below).
3. Run:

```
cd src/img_comp_engine
uv run python main.py
```

The result is written to `output/composition.png`.

> **Note:** all images must have exactly the same dimensions. Otherwise the program stops and tells you which layer has the wrong size.

## Configuration

Here is an example `conf.yml`:

```yaml
layers:
  - image: stones.jpg          # background layer
    filters:
      - name: gaussianblur
        params:
          window: 11
          sigma: 3.0
  - image: colors.jpg
    filters:
      - name: brightness
        params:
          level: 0.1
    blend: difference
    opacity: 0.4
  - image: animal.jpg
    filters:
      - name: invert
    blend: normal
    opacity: 0.7
```

Each layer accepts:

| Key | Required | Default | Description |
|-----|----------|---------|-------------|
| `image` | yes | | File name inside `Images/` |
| `filters` | no | none | List of filters, applied in order |
| `blend` | no | `normal` | How the layer is mixed with what is below |
| `opacity` | no | `1.0` | Number between 0 (invisible) and 1 (fully visible) |

### Filters

| Name | Parameters | What it does |
|------|-----------|--------------|
| `grayscale` | none | Converts to grayscale, weighting channels by perceived brightness |
| `brightness` | `level` | Adds `level` to every value (negative = darker) |
| `contrast` | `factor` (≥ 0) | Stretches values around mid-gray: above 1 = more contrast, below 1 = less |
| `gaussianblur` | `window` (odd integer), `sigma` (> 0) | Blurs the image. `window` is the size of the blur area, `sigma` its strength |
| `invert` | none | Inverts the colors |

### Blend modes

| Name | Effect |
|------|--------|
| `normal` | The layer is placed over the background |
| `difference` | Absolute difference between the layer and the background |
| `multiply` | Multiplies both images: the result is darker |
| `lighten` | Keeps the lighter pixel of the two |

In every mode, `opacity` controls how much of the effect is mixed into the background.

## Project structure

```
Image-Composition-Engine/
├── pyproject.toml
│
└── src/img_comp_engine/
    ├── main.py       # entry point: converts conf.yml, runs the engine, prints errors
    ├── config.py     # YAML to JSON conversion
    ├── engine.py     # reads the config, builds the layers, composes the final image
    ├── layer.py      # Layer: image + filters + opacity + blend mode
    ├── filters.py    # filter classes
    ├── blend.py      # blend mode classes
    ├── images.py     # loading and saving images
    ├── conf.yml      # your layer description
    ├── Images/       # input images
    └── output/       # result
```

`config.json` is generated from `conf.yml` every time you run the program, so you never need to edit it.

## Adding your own filter or blend mode

1. Create a class in `filters.py` (or `blend.py`) with an `apply` method.
2. Add one line to the `FILTERS` (or `BLENDS`) dictionary in `engine.py`.

```python
class SepiaFilter(Filter):
    def apply(self, img):
        ...

# engine.py
FILTERS = {
    ...
    "sepia": SepiaFilter,
}
```

You can then use `name: sepia` in `conf.yml`.

## Error messages

The program checks your configuration and stops with a clear message instead of crashing, for example:

- unknown filter or blend mode
- missing filter parameter (e.g. no `sigma` for a blur)
- opacity outside the 0 to 1 range
- missing image file
- images with different dimensions

## Test another filters file 

Our trinome was Chloe/Pierre and Hugo/Thomas

To use the additional filters (from the other team) simply disactivate the original filters
and activate the other team's filters in the filter.py file. Then in main.py, activate the 
alternative .json path and disactivate the original.  Once the Thomas_config file is modified
for the images, filters, and parameters you want, simply run the main.py file and your 
new image will be saved to the output folder.