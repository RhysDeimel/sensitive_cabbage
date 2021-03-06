import imagehash
import logging
import requests
import sqlite3
import os
from PIL import Image, ImageFont

from io import BytesIO

import time

import tempfile

logging.basicConfig(level=logging.DEBUG)

# given a reddit user, leverage pushshift to iterate through content and archive
USER = ""  # TODO - make this a commandline arg
URL = "https://api.pushshift.io/reddit/search/submission/"

# create user directory
# if not os.path.exists(USER):
#     logging.debug(f" User: {USER} does not exist, creating folder.")
#     os.mkdir(USER)

# if not os.path.exists(f"{USER}/posts.db"):
#     logging.debug(f" User: {USER} does not have a post record. Creating.")
#     # create DB for reference
#     conn = sqlite3.connect(f"{USER}/posts.db")
#     c = conn.cursor()
#     c.execute(
#         """
# 		CREATE TABLE posts (id text, created_utc integer, title text, hash text, duplicate integer)
# 		"""
#     )
#     conn.commit()
#     conn.close()

# check db for most recent record
# "SELECT * FROM posts ORDER BY created_utc DESC LIMIT 1"

# iterate through pushshift and last record till current time
# check if post is duplicate
# if not, download image and check if hash already exists and dedupe
# save hash
# Add title text to bottom of image


# Get dimensions of image, make a new blank image that is larger, then
# paste the old image over it. This should give white space at the bottom
# to add the title text.
# https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.paste

# first_img = Image.open("in.jpg")
# w,h = first_img.size
# second_img = Image.new("RGB", (w,h+(h//4)), "white")
# second_img.paste(first_img)
# second_img.save("out.jpg")


# to render text
# im = Image.new('RGB', (400,400), "white")
# draw = ImageDraw.Draw(im)
# font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 38, encoding="unic")
# draw.text((10,10), "hello", (0,0,0), font=font)
# im.save("out.jpg")

# binary search-like method to adjust font size based on image width
# breakpoint = img_fraction * photo.size[0]
# jumpsize = 75
# while True:
#     if font.getsize(text)[0] < breakpoint:
#         fontsize += jumpsize
#     else:
#         jumpsize = jumpsize // 2
#         fontsize -= jumpsize
#     font = ImageFont.truetype(font_path, fontsize)
#     if jumpsize <= 1:
#         break


def calc_font_size(image, text):
    """
    Calculate size based on height of image

    returns: font object with desired size
    """

    path = "/usr/share/fonts/truetype/freefont/FreeSans.ttf"
    fontsize = 1
    jumpsize = 75
    breakpoint = 0.03 * image.size[1]  # use image height

    font = ImageFont.truetype(path, fontsize, encoding="unic")
    while True:
        print(f"{fontsize} {jumpsize}: ", end="")
        if font.getsize(text)[1] < breakpoint:
            fontsize += jumpsize
            print("increasing")
        else:
            print("decreasing")
            jumpsize //= 2
            fontsize -= jumpsize

        font = ImageFont.truetype(path, fontsize, encoding="unic")

        if jumpsize <= 1:
            print("exiting")
            break

    return font


def break_text_into_lines(text, image, font):
    """
    Given a font size, and the image, take the width and break text into lines that will
    fit within the image
    """

    # for a given amount of text:
    #   split into individual words
    #   add one word at a time, checking length. If length is > desired width,
    #       add a line break before that word then reset length checking counter and continue
    # then call draw.multiline_textsize(text) to get the x,y dimensions
    # add the y onto the bottom of the image
    words = text.split(" ")
    maxwidth = image.width - 50

    draw = ImageDraw.Draw(image)

    line = []
    for position, word in enumerate(words):
        line.append(word)

        if draw.textsize(" ".join(line), font)[0] >= maxwidth:
            words[position] = "\n" + word

            line = [word]

    return " ".join(words)


class Picture:
    def __init__(self, content, title, created_utc):
        self.i = Image.open(BytesIO(content))
        self.hash = imagehash.average_hash(self.i)

        self.title = title
        self.created_utc = created_utc
        self.fontsize = 1

    @property
    def font(self):
        path = "/usr/share/fonts/truetype/freefont/FreeSans.ttf"
        return ImageFont.truetype(path, self.fontsize, encoding="unic")

    def generate(self):
        # generates font, updates image, and saves to disk
        pass


class Video:
    def __init__(self):
        pass


# # Some ghetto code testing out pushshift
# end = int(time.time())
# start = end - 86400
# # go backwards
# while True:
#     r = requests.get(URL + f"?author={USER}&after={start}&before={end}&size=100&sort=asc")
#     data = r.json()["data"]
#     if not data:
#         break

#     for post in data:
#             download(post["url"], name=post["created_utc"])

#         if not is_duplicate():
#             add_text(post["title"])
#         else:
#             delete(post["created_utc"])

#         record_details(post)

#     end = start
#     start -= 86400

if __name__ == "__main__":
    url = "http://localhost:8000/in.jpg"
    title = (
        "Pilots of the 120th Air Defense Fighter Aviation Regiment take an oath to the Guards banner."
        " The 120th Fighter Aviation Regiment became the 12th Guards Fighter Aviation Regiment."
        " Behind the personnel are MiG-3 fighters, with which the 120th Air Defense IAP (12th Air "
        "Defense GIAP) of the city of Mos"
    )
    created = int(time.time())
    
    r = requests.get(url)

    test = Picture(r.content, title, created)




# to check hash of image:

# from PIL import Image
# import imagehash
# hash0 = imagehash.average_hash(Image.open('quora_photo.jpg')) 
# hash1 = imagehash.average_hash(Image.open('twitter_photo.jpeg')) 
# cutoff = 5

# if hash0 - hash1 < cutoff:
#   print('images are similar')
# else:
#   print('images are not similar'