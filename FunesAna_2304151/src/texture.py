import numpy as np

class ImageData:
    def __init__(self, height, width, channels, color =(0,0,0)):
        self.data = np.full((height, width, channels), color, dtype=np.uint8)

    def set_pixel(self, x, y, color):
        self.data[y, x] = color

    def tobytes(self):
        return self.data.tobytes()

class Texture:
    def __init__(self, name = "u_texture", width = 1, height = 1, channels_amount = 4, image_data = None, 
                color = (0,0,0),repeat_x = False, repeat_y = False, build_mimaps = False):
        self.name = name
        self.size = (width, height)
        self.channels_amount = channels_amount
        self.__image_data = image_data.tobytes() if image_data is not None else None
        self.repeat_x = repeat_x
        self.repeat_y = repeat_y
        self.build_mipmaps = build_mimaps

        self.width = width
        self.height = height

        if image_data is None:
            self.__image_data = ImageData(height, width,channels_amount, color)
        else:
            self.__image_data = image_data

    @property
    def image_data(self):
        return self.__image_data
    
    def update_data(self, new_data: ImageData):
        self.__image_data = new_data

    def set_pixel(self,x,y,color):
        self.__image_data.set_pixel(x,y,color)

    def get_bytes(self):
        return self.__image_data.tobytes()