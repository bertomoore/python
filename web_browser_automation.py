from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from re import search
import json
import time



specialchar = ['"', "'", "_", ":", "-", " "]
hash_map    = {}
init_count  = 0
art_count   = 0
year        = 2008



def charStrip(raw_link):
    return "".join([x for x in raw_link if x not in specialchar]).lower()



static = "C:/Users/Berto/sarajenkinsart/static/"
with open(static + "artwork.json", "r+") as final:
    json_dict = json.loads(final.readline())

    for title in json_dict:
        hash_map[charStrip(title)[:-4]] = title
        init_count += 1

    print(x for x in hash_map.keys())

    browser  = webdriver.Firefox()

    while year <= 2018:
        browser.get("https://search.verizonwireless.com/onesearch/search?q=galaxy+note9")
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
            title_words = charStrip(search(r'(?<=art/)[-_a-zA-Z0-9\'"\?!~]+(?=-[0-9]{3,})', img_links[x]).group())

            if title_words in hash_map:
                art_count += 1                
                print(str(art_count) + ": " + hash_map[title_words] + "\n")
                json_dict[hash_map[title_words]]["year"] = str(year)

            else:
                print(title_words, "is not in hashmap\n")

        year += 1

    for x in json_dict:
        if int(json_dict[x]["year"]) < 2008 :
            print(json_dict[x]["name"])

    json.dump(json_dict, final)
    final.close()

print("Total number of updated arwork:", str(art_count))