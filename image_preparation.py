import os
import tqdm
import math
from PIL import Image


def resize_image(infile, outfile):
    size = 48, 48
    img = Image.open(infile)

    # make image roughly square
    longer_side = max(img.size)
    horizontal_padding = math.ceil((longer_side - img.size[0]) / 2.)
    vertical_padding = math.ceil((longer_side - img.size[1]) / 2.)
    im = img.crop(
        (
            -horizontal_padding,
            -vertical_padding,
            img.size[0] + horizontal_padding,
            img.size[1] + vertical_padding
        )
    )
    # turn into smaller
    im.thumbnail(size, Image.ANTIALIAS)

    # # handle in case 1 dimension slightly off by 1
    # longer_side = max(im.size)
    # horizontal_padding = (longer_side - img.size[0]) / 2
    # vertical_padding = (longer_side - img.size[1]) / 2
    # im = img.crop(
    #     (
    #         -horizontal_padding,
    #         -vertical_padding,
    #         img.size[0] + horizontal_padding,
    #         img.size[1] + vertical_padding
    #     )
    # )
    im.save(outfile, "JPEG")


def resize_all_images():
    """Resizes all images in the photos/ directory and stores them as
    48x48 jpg images in the processed/ directory"""
    if not os.path.exists('processed'):
        os.makedirs('processed')
    files = os.listdir('photos')
    for file in tqdm.tqdm(files):
        infile = 'photos/{}'.format(file)
        outfile = 'processed/{}.jpg'.format(file.split('.')[0])
        try:
            resize_image(infile, outfile)
        except:
            # some downloaded files are just html, not images
            pass


if __name__ == '__main__':
    resize_all_images()