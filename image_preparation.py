import os
from PIL import Image


def resize_image(infile, outfile):
    size = 48, 48
    im = Image.open(infile)
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(outfile, "JPEG")


def resize_all_images():
    """Resizes all images in the photos/ directory and stores them as
    48x48 jpg images in the processed/ directory"""
    if not os.path.exists('processed'):
        os.makedirs('processed')
    files = os.listdir('photos')
    for file in files:
        infile = 'photos/{}'.format(file)
        outfile = 'processed/{}.jpg'.format(file.split('.')[0])
        try:
            resize_image(infile, outfile)
        except:
            # some downloaded files are just html, not images
            pass


if __name__ == '__main__':
    resize_all_images()