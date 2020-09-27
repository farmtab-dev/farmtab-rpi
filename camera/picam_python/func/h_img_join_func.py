# https://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python/46623632#46623632
# https://note.nkmk.me/en/python-numpy-image-processing/#:~:text=Image%20.-,PIL.,image%20file%20with%20save()%20.&text=You%20can%20write%20it%20in%20one%20line.&text=If%20the%20data%20type%20dtype,it%20as%20JPG%20or%20PNG.
from PIL import Image
import os

def join_images(*rows, bg_color=(0, 0, 0, 0), alignment=(0.5, 0.5)):
    rows = [
        [image.convert('RGBA') for image in row]
        for row
        in rows
    ]

    heights = [
        max(image.height for image in row)
        for row
        in rows
    ]

    widths = [
        max(image.width for image in column)
        for column
        in zip(*rows)
    ]

    tmp = Image.new(
        'RGBA',
        size=(sum(widths), sum(heights)),
        color=bg_color
    )

    for i, row in enumerate(rows):
        for j, image in enumerate(row):
            y = sum(heights[:i]) + int((heights[i] - image.height) * alignment[1])
            x = sum(widths[:j]) + int((widths[j] - image.width) * alignment[0])
            tmp.paste(image, (x, y))

    return tmp


def join_images_horizontally(*row, bg_color=(0, 0, 0), alignment=(0.5, 0.5)):
    return join_images(
        row,
        bg_color=bg_color,
        alignment=alignment
    )


def join_images_vertically(*column, bg_color=(0, 0, 0), alignment=(0.5, 0.5)):
    return join_images(
        *[[image] for image in column],
        bg_color=bg_color,
        alignment=alignment
    )

def getExistImgFilepath(fp,img_size):
    return  Image.open(fp) if   os.path.exists(fp) else Image.new('RGBA', img_size, (255,255,255,0))

def get4X4ImgMerged(dirpath, filepath_A, filepath_B, filepath_C, filepath_D):
    img_size = Image.open(filepath_A).size
    print(img_size) # https://www.tutorialspoint.com/python_pillow/python_pillow_imagedraw_module.htm
    images = [
        [getExistImgFilepath(filepath_A,img_size), getExistImgFilepath(filepath_B,img_size)],
        [getExistImgFilepath(filepath_C,img_size), getExistImgFilepath(filepath_D,img_size)],
    ]
    fp = dirpath + '/' + "COMBINED.png"
    join_images(*images, bg_color='green', alignment=(1, 1)).save(fp)
    print(fp)
    return fp