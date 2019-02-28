'''
Script to obtain URLs for smartphones, then loop through
each page to obtain needed info. Used for phone comparison app
'''


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.request import urlretrieve
from re import search
import json
from time import sleep

browser  = webdriver.Chrome()
browser.get("https://www.verizonwireless.com/smartphones/")
sleep(2.0)

links = browser.execute_script("""
    var final = {};
    var links = $(".NHaasTX75Bd > a");
    for (var x=0; x<links.length;x++) {
        if (links[x].href.indexOf("certified")==-1) final[links[x].innerText.replace(/ with Sapphire Shield| V (2nd|3rd) Gen|[^A-Za-z0-9+ ]/ig,"")] = links[x].href;
    }
    return final;
""")

phone_data = {}

with open("phone.json") as w:
    phone_data = json.loads(w.readline())
    
    for name in links:

        phone_name = " ".join(name.replace(" Plus","+").split(" ")[1:])
        if phone_name not in phone_data: continue
        print(phone_name,"is up next!")
        browser.get(links[name])

        urlretrieve(browser.execute_script("return $('.image-gallery-image img')[0].src"),"photos/{}.jpg".format(phone_name))

        phone_colors = browser.execute_script("""
            var final = {};
            var colors = $("input[name='colors']");
            for (var y=0;y<colors.length;y++) {
                final[colors[y].value] = colors[y].id;
            }

            return final;
        """)

        phone_data[phone_name]["Colors"] = phone_colors

with open("phone.json","w") as w: json.dump(phone_data,w)