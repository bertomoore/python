'''
A script to make resized version of images for desktop
and mobile icons
'''

from PIL import Image, ImageFile
import json

static  = 'sarajenkinsart/static/'
artJSON = {}

with open(static + 'artwork.json') as f:
    artlist = json.loads(f.readline())

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
mobile_width = 860
thumb_width = 500
quality = 80

for x in artlist:
    img = Image.open("pictures/sara-art-backup" + "/" + artlist[x])
    mobile_wper = mobile_width / float(img.size[0])
    mobile_height = int(float(img.size[1] * mobile_wper))
    mobile_img = img.resize((mobile_width, mobile_height), Image.ANTIALIAS)
    mobile_img.save('sarajenkinsart/mobile' + artlist[x])
    mobile_wper = mobile_width / float(img.size[0])
    mobile_height = int(float(img.size[1] * mobile_wper))
    mobile_img = img.resize((mobile_width, mobile_height), Image.ANTIALIAS)
    mobile_img.save('sarajenkinsart/desktop' + artlist[x])

with open(static + 'artwork.json', 'w') as f:
    json.dump(artJSON, f)