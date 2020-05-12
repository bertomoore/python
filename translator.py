from selenium import webdriver
from time import sleep
import os

phrases = []

for r, d, f in os.walk("./locales"):
    language_files = f
    break

browser = webdriver.Chrome()

for filename in language_files:

    with open("locales/" + filename) as f:
        file_lines = f.readlines()
        file_lines[-2] = file_lines[-2][:-2] + '",\n'

    language = filename[:2] if filename[0] != 'z' else filename[:5]
    
    for phrase in phrases:
        browser.get(f"https://translate.google.com/#view=home&op=translate&sl=en&tl={language}&text={phrase.replace(' ','%20')}")
        sleep(2.0)
        translation = browser.execute_script("return document.getElementsByClassName('translation')[0].innerText")
        file_lines.insert(-1, f'  "{phrase}": "{translation}"{"," if phrase != phrases[-1] else ""}\n')

    with open("locales/" + filename, "w") as w:
        w.writelines(file_lines)