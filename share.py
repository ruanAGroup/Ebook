import os
import random
from PIL import Image, ImageFont, ImageDraw
from PIL.ImageQt import ImageQt

from basic import strListToString


def vertical_write(book_info_strs, drawobj, font, color, x):
    W, H = 365, 458
    row_hight = 0  # 行高设置（文字行距）
    word_dir = 10  # 文字间距
    right = 0  # 往右位移量
    down = -20  # 往下位移量
    i = 0
    w, h = font.getsize(book_info_strs[0])  # 获取第一个文字的宽和高
    num_h = len(book_info_strs)
    while i < len(book_info_strs):
        char = book_info_strs[i]
        if char == "," or char == "\n":
            right = right + w + row_hight
            down = -20
            continue
        elif char == '[':  # 遇到[]符号时，合并三个字符
            char = book_info_strs[i:i + 3]
            i += 2
            num_h -= 2  # 字数减二(计算高度用)
        elif i == 0:
            down = -20
        else:
            down = down + h + word_dir
        i += 1
        height = num_h * h + word_dir * (num_h - 1)
        y = (H - height) / 2
        drawobj.text((x + right, y + down), char, font=font, fill=color)  # 设置位置坐标 文字 颜色 字体


def template_first(template, book, color):
    W, H = 365, 458
    im = Image.open(template)
    drawobj = ImageDraw.Draw(im)
    book_name = book.name
    font = ImageFont.truetype('./fonts/方正咆哮体.TTF', 38)  # 选取字体为方正咆哮体, 36号
    w, h = drawobj.textsize(book_name, font=font)
    drawobj.text(((W - w) / 2, 110), book_name, font=font, fill=color[1])

    authors = strListToString(book.authors)
    font = ImageFont.truetype('./fonts/SIMSUN.TTC', 13)  # 选取字体为宋体, 13号
    w, h = drawobj.textsize(authors, font=font)
    drawobj.text(((W - w) / 2, 250), authors, font=font, fill=color[2])

    publisher = book.publisher
    font = ImageFont.truetype('./fonts/华文细黑.ttf', 12)  # 选取字体为华文细黑, 12号
    w, h = drawobj.textsize(publisher, font=font)
    drawobj.text(((W - w) / 2, 380), publisher, font=font, fill=color[3])
    return im


def template_second(template, book, color):
    W, H = 365, 458
    im = Image.open(template)
    drawobj = ImageDraw.Draw(im)
    book_name = book.name
    font = ImageFont.truetype('./fonts/方正喵呜体.TTF', 38)  # 选取字体为方正喵呜体, 38号
    vertical_write(book_name, drawobj, font, color[1], 120)  # 竖写

    authors = strListToString(book.authors)
    font = ImageFont.truetype('./fonts/SIMSUN.TTC', 13)  # 选取字体为宋体, 13号
    vertical_write(authors, drawobj, font, color[2], 250)  # 竖写

    publisher = book.publisher
    font = ImageFont.truetype('./fonts/华文细黑.ttf', 12)  # 选取字体为华文细黑, 12号
    w, h = drawobj.textsize(publisher, font=font)
    drawobj.text(((W - w) / 2, 380), publisher, font=font, fill=color[3])
    return im


def getRandomColorGroup():
    color_list = [
        ['#87CEFA', '#FF4500', '#8B4513', '#663366'],
        ['#FF6633', '#33FF66', '#33CCFF', '#333366'],
        ['#ffff66', '#666600', '#3333FF', '#663366'],
    ]  # 配色集
    num = random.randint(0, len(color_list)-1)
    return color_list[num]


def getRandomTemplate():
    if not os.path.exists('templates'):
        os.mkdir('templates')
    pics = []
    for file in os.listdir('templates'):
        if file.endswith(('.jpg', '.png', '.jpeg', '.bmp')):
            pics.append(file)
    num = random.randint(0, len(pics)-1)
    return os.path.join('templates', pics[num])


def text2picture(book):
    mode = random.randint(0, 1)
    if mode == 0:
        im = template_first(getRandomTemplate(), book, getRandomColorGroup())
    else:
        im = template_second(getRandomTemplate(), book, getRandomColorGroup())
    qtimg = ImageQt(im)
    return qtimg
