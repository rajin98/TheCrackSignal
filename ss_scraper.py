import base64
import face_recognition.face_recognition as fr
from selenium import webdriver
import draw_box
import os
from selenium.webdriver.chrome.options import Options
import time

dir_name = 'michael'

image_dir = os.listdir(dir_name)
known_images = [fr.load_image_file(dir_name+'/'+i) for i in image_dir if i.endswith('.jpg')]
known_encodings = []

for image in known_images:
    temp = fr.face_encodings(image)
    if len(temp) > 0:
        known_encodings.append(temp[0])


chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")

js = open("set_res.js")

def isPersonThere(im):
    arg_encoding_arr = fr.face_encodings(im)
    if len(arg_encoding_arr) > 0:
        arg_encoding = arg_encoding_arr[0]
    else:
        return False

    # result = fr.compare_faces([known_encoding], arg_encoding)
    results = fr.compare_faces(known_encodings, arg_encoding)
    return True in results


def scrapFromTwitch(url, fn):
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)

    # el = driver.find_element_by_css_selector('button[data-a-target="player-settings-button"]')
    # el.click()
    # el = driver.find_element_by_css_selector('button[data-a-target="player-settings-menu-item-quality"]')
    # el.click()
    # el = driver.find_element_by_css_selector('div[data-a-target="player-settings-submenu-quality-option"] input:first-child')
    # el.click()
    driver.execute_script(js.read())

    i = 0
    while i < 10:
        time.sleep(10)
        ss_script = open("take_ss.js")
        driver.execute_script(ss_script.read())
        dl = driver.find_element_by_id('selenium-download-link')
        image64 = dl.get_attribute('href')
        image64 = image64[23:]

        with open(fn, 'wb') as f:
            f.write(base64.b64decode(image64))

        print(isPersonThere(fr.load_image_file(fn)))
        draw_box.drawRectangle(fr.load_image_file(fn))
        # os.remove(filename)
        i += 1

    driver.close()


filename = 'ss.jpg'
link = "https://www.twitch.tv/videos/556436677?t=5h20m40s"
# link = "https://www.twitch.tv/lilypichu"
scrapFromTwitch(link, filename)

