import os
import random
from PIL import Image, ImageFont, ImageDraw
from PIL.ImageQt import ImageQt

from basic import strListToString


def getRandomFont():
    if not os.path.exists('fonts'):
        os.mkdir('fonts')
    fonts = []
    for file in os.listdir('fonts'):
        if file.endswith(('.ttf', '.ttc', '.TTF')):
            fonts.append(file)
    num = random.randint(0, len(fonts)-1)
    return os.path.join('fonts', fonts[num])


def getRandomColor():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b


def getRandomTemplate():
    if not os.path.exists('templates'):
        os.mkdir('templates')
    pics = []
    for file in os.listdir('templates'):
        if file.endswith(('.jpg', '.png', '.jpeg', '.bmp')):
            pics.append(file)
    num = random.randint(0, len(pics)-1)
    return os.path.join('templates', pics[num])


def convertText(text, num):
    if len(text) <= num:
        return text
    textlist = [text[i:i+num] for i in range(0, len(text), num)]
    return "\n".join(textlist)


def template_first(template, book):
    W, H = 365, 458
    im = Image.open(template)
    drawobj = ImageDraw.Draw(im)
    book_name = convertText(book.name, 6)
    font = ImageFont.truetype(getRandomFont(), 40)
    drawobj.text((10, 10), book_name, font=font, fill=getRandomColor())

    authors = strListToString(book.authors)
    font = ImageFont.truetype(getRandomFont(), 20)
    drawobj.text((10, 250), authors, font=font, fill=getRandomColor())

    publisher = book.publisher
    font = ImageFont.truetype(getRandomFont(), 18)  # 选取字体为华文细黑, 12号
    drawobj.text((10, 380), publisher, font=font, fill=getRandomColor())
    return im


def generateCover(book):
    return template_first(getRandomTemplate(), book)


def getCover(book):
    img = generateCover(book)
    qtimg = ImageQt(img)
    return qtimg
