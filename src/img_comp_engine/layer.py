from img_comp_engine.images import array_from_file

class Layer: 
    def __init__(self,image_path:str,filtres):
        self.image_name = image_path
        self.img = array_from_file(image_path)
        self.filters = filtres