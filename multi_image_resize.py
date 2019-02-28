from PIL import Image, ImageFile
from os import getcwd, walk
from re import search, I

### Automation tool to resize images found on sarajenkinsart.com

art_dir = "../sarajenkinsart/static/"

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
base_max  = 2000



for root, dirs, photo in walk(art_dir):
    if root == art_dir + "thumb" or root == art_dir + "font" or root == art_dir:
        continue

    else:
        for x in range(len(photo)):
            if search(r'\.(jpeg|jpg|png|gif)', photo[x], I) is not None:
                with Image.open(root + "/" + photo[x]) as this_image:

                    if this_image.size[0] > 2000 or this_image.size[1] > 2000:
                        if this_image.size[0] > this_image.size[1]:
                            this_image = this_image.resize((base_max, int(float(this_image.size[1])*base_max/float(this_image.size[0]))), Image.ANTIALIAS)
                        else:
                            this_image = this_image.resize((int(float(this_image.size[0])*base_max/float(this_image.size[1])), base_max), Image.ANTIALIAS)

                        print(photo[x], this_image.size[0], 'x', this_image.size[1])
                        this_image.save(root + '/' + photo[x])

                    else:
                        print(photo[x], 'is already less than 2000 x 2000')