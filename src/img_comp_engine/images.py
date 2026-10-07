from pathlib import Path

import numpy as np
from PIL import Image

import scipy.ndimage
from pathlib import Path


def array_from_file(path: str | Path) -> np.ndarray:
    """Charge une image et la renvoie en tableau RGB entre 0 et 1."""
    with Image.open(path) as image:
        return np.asarray(image.convert("RGB"), dtype=np.float32) / 255.0

def array_to_img(arr: np.ndarray):
    '''Convertit un tableau de valeur entre 0 et 1 en image Pillow.'''
    adjusted =  np.array(np.clip(arr, 0, 1) * 255, dtype=np.uint8)
    pil_img = Image.fromarray(adjusted)
    return pil_img

def show_from_array(arr: np.ndarray):
    '''Affiche un tableau comme une image.'''
    img = array_to_img(arr)
    img.show()

#def np_img_to_pil(img):
    #verify that RGB values don't exceed 255
    #clipped = np.clip(img,0,1)
    #normalized_img = np.array (clipped *255, dtype= np.uint8)
    #pil_img = Image.fromarray(normalized_img)
    #return pil_img

def save_img(img: np.ndarray, outname: str):
        #image between 0 and 1
        pil_img = array_to_img(img)
        pil_img.save(outname)


    