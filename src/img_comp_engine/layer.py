from img_comp_engine.images import array_from_file, show_from_array, save_img

class Layer:
    def __init__(self,name,filters):
          #load the image
          self.img: np.ndarray = array_from_file(name)
          self.filters: list[Filter] = filters
          self.name: str = name