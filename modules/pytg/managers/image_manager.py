import telegram, os

import urllib.request

# Images
def download_image(image_id, image_url):
    image_data = urllib.request.urlopen(image_url).read()

    with open("data/images/{}".format(image_id), "wb") as image_file:
        image_file.write(image_data)

    return image_data

def load_image(image_id):
    return open("data/images/{}".format(image_id), "rb")