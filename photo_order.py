'''
A script used to obtain image sources and their respective
order on the dom. Many of the photos only displayed after
scrolling, hence the need to use web driver software instead
of a simple http get request.
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from re import search
import json
import time



special_char = ['"', "'", "_", ":", "-", " "]
art_count = 0
result = []

def char_strip(raw_link):
    return "".join([x for x in raw_link if x not in special_char]).lower()

with open("photo_order.txt", "w") as photo_order:
    browser  = webdriver.Firefox()
    browser.get("https://udavrajati.deviantart.com/gallery/")
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2.0)

        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

        last_height = new_height

    img_links  = browser.execute_script("""
        images = document.getElementsByClassName('torpedo-thumb-link');
        result = [];
        for (var x=0; x < images.length; x++) result.push(images[x].getAttribute("href"));
        return result;
    """)

    for x in range(len(img_links)):
        result.append(img_links[x] + "\n")

    photo_order.writelines(result)