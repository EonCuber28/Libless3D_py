from PIL import Image
import numpy as np

def load_texture(texture_id):
    try:
        texture_path = "C:/Users/zappa/Desktop/Libless3D/Libless3D_py/assets/textures/"+texture_id
        texture = np.array(Image.open(texture_path).convert("RGB"))
    except:
        try:
            texture_path = "E:/Libless3D/assets/textures/"+texture_id
            texture = np.array(Image.open(texture_path).convert("RGB"))
        except:
            texture_path = "/media/pi/LIBLESS3D/Libless3D/assets/textures/"+texture_id
            texture = np.array(Image.open(texture_path).convert("RGB"))
    return texture

def resize_texture(texture, new_width=64,new_height=64):
    img = Image.fromarray(texture.astype(np.uint8))
    img = img.resize((new_width, new_height), resample=Image.BILINEAR)
    return np.array(img)
