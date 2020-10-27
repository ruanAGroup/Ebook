from PIL import Image
from PIL.ImageQt import ImageQt


def example(title="", author="", publisher=""):
    img = Image.open('templates/1.png')
    # 给img添加文字
    qtimg = ImageQt(img)
    return qtimg
