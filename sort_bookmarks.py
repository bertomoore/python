'''
A bookmark sorting script I created for my manager using regex.
Some of the original data has been removed for privacy reasons.
Add names to folder_category and use regex for loop on line 29.
'''

import re
import time
from bs4 import BeautifulSoup

folder_category = {
    # "School" : []
}

current_bookmark_file = "" # Add bookmark path here

with open(current_bookmark_file) as f:
    data = BeautifulSoup("".join(f.readlines()),"html.parser")

for a in data.find_all("a"):
    # if re.search("\.edu|university|unm|class",a,re.I):
    #     folder_category["School"].append(a)

final = BeautifulSoup("""
<!DOCTYPE NETSCAPE-Bookmark-file-1>

<!--This is an automatically generated file. 
    It will be read and overwritten. 
    Do Not Edit! -->
<title>Bookmarks</title>
<h1>Bookmarks</h1>
<dl>
</dl>
""","html.parser")

bookmark_count = 0
first_folder = True

for title in categories:

    if first_folder:
        folder_tag = final.dl
        first_folder = False

    else:
        folder_tag = final.find_all("dts")[-1]

    folder_tag.append(data.new_tag("p"))
    folder_tag.find_all("p")[-1].append(data.new_tag("dts"))

    dt = final.find_all("dts")[-1]
    bookmark_count = 0

    header = data.new_tag("h3", add_date=int(time.time()), folded="")
    header.string = title

    dt.append(header)
    dt.append(data.new_tag("dl"))
    dt.dl.append(data.new_tag("p"))

    for bookmark in folder_category[title]:
        current_tag = dt.dl.p if not(bookmark_count) else final.find_all("dt")[-1]
        current_tag.append(data.new_tag("dt"))

        try:
            new_bookmark = data.new_tag("a",
                add_date=bookmark["add_date"],
                href=bookmark["href"],
                icon_uri=bookmark["icon_uri"],
                last_modified=bookmark["last_modified"],
                last_visit=bookmark["last_visit"]
            )

        except:
            new_bookmark = data.new_tag("a",
                add_date=bookmark["add_date"],
                href=bookmark["href"],
                last_modified=bookmark["last_modified"],
                last_visit=bookmark["last_visit"]
            )

        new_bookmark.string = bookmark.string
        current_tag.dt.append(new_bookmark)

        bookmark_count += 1

with open("new_bookmarks.html","w") as w:
    w.write(re.sub("dts","dt",str(final)))