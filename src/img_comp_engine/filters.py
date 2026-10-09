from abc import ABC, abstractmethod
import numpy as np
from scipy.ndimage import convolve1d
         

class Filter(ABC):
    def __init__(self,params=None):
        pass

    @abstractmethod
    def apply(self, img: np.ndarray) -> np.ndarray:
        ''' Applique le filtre et renvoie une image sous forme de tableau'''
        raise NotImplementedError
    
    

class BrightnessFilter(Filter):
    def __init__(self,params):
        self.level = params["level"]

        if "level" not in params:
            raise ValueError ("must specify brightness level")
    def apply(self,img :np.ndarray) -> np.ndarray:
        
        return np.clip(img + self.level, 0.0, 1.0)

    

class GrayscaleFilter(Filter):
    def apply(self,img: np.ndarray) -> np.ndarray:
        # moyenne pondérée : l'oeil voit plus le vert que le bleu
        gray = 0.299 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 2]
        return np.stack((gray, gray, gray), axis=-1)



class GaussianBlurFilter(Filter):
    def __init__(self, params):
        self.window = params["window"]
        self.sigma = params["sigma"]

<<<<<<< HEAD
        if "window" not in params:
            raise ValueError ("must specify window for Gaussian blur")

        if "sigma" not in params:
            raise ValueError ("must specify sigma for Gaussian blur")
                        
        if type(self.window) is not int or self.window <= 0 or self.window % 2 == 0:
            raise ValueError("window must be possitive and odd")
=======
        if not isinstance(self.window, int) or self.window <= 0 or self.window % 2 == 0:
            raise ValueError("window doit être un entier positif impair")
>>>>>>> 95f169e4206b8f45a89d49aff18a301fe3a296a6

        if self.sigma <= 0:
            raise ValueError("sigma must be positive")
        

    def apply(self, img: np.ndarray) -> np.ndarray:
        radius = self.window // 2
        x = np.arange(-radius, radius + 1)

        # noyau 1D : on floute d'abord les lignes, puis les colonnes
        kernel = np.exp(-(x**2) / (2 * self.sigma**2))
        kernel /= kernel.sum()

        blurred = convolve1d(img, kernel, axis=0, mode="reflect")
        blurred = convolve1d(blurred, kernel, axis=1, mode="reflect")
        return blurred



class InvertFilter(Filter):
    def apply(self,img: np.ndarray) -> np.ndarray:
        return 1.0 - img


class ContrastFilter(Filter):
    def __init__(self,params):
        self.factor = params["factor"]

        if "factor" not in params:
            raise ValueError ("must specify contrast factor")
        if self.factor <0:
            raise ValueError("factor must be greater than or equal to 0")
        
        
    def apply(self,img: np.ndarray) -> np.ndarray :
        return np.clip((img - 0.5) * self.factor + 0.5, 0.0, 1.0)
    








