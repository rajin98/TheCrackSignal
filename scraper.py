import base64
import face_recognition as fr
from selenium import webdriver
import draw_box
import os
import requests
from selenium.webdriver.chrome.options import Options

DEBUG = False
GLOBAL_STATE = False


def scrapFromTwitch(url, fn, chrome_options, channel, known_encodings):
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    js = open("set_res.js")
    driver.execute_script(js.read())

    # i = 0
    while isLive(channel) or DEBUG:

        ss_script = open("take_ss.js")
        driver.execute_script(ss_script.read())
        dl = driver.find_element_by_id('selenium-download-link')
        image64 = dl.get_attribute('href')
        image64 = image64[23:]

        with open(fn, 'wb') as f:
            f.write(base64.b64decode(image64))

        result = draw_box.drawRectangle(fr.load_image_file(fn), known_encodings)
        print(result[0])
        sendData(result[0], result[1], channel)
        # os.remove(filename)
        # i += 1

    driver.close()
    sendEndofStream()


def sendData(status, image, channel):
    url = 'http://cracksignal.scienceontheweb.net/api/admin/update.php/'
    if DEBUG:
        url = 'http://192.168.0.13/crackSignal/api/admin/update.php/'
    data = {'auth': '<authentication-key>', 'status': status, 'image': image, 'channel': channel}
    r = requests.post(url=url, data=data)


def sendEndofStream():
    url = 'http://cracksignal.scienceontheweb.net/api/admin/update.php/'
    if DEBUG:
        url = 'http://192.168.0.13/crackSignal/api/admin/update.php/'
    data = {'auth': '<authentication-key>', 'status': False, 'image': False, 'channel': False, 'eos': True}
    r = requests.post(url=url, data=data)

def isLive(channel):
    url = 'https://api.twitch.tv/helix/streams?user_login=' + channel
    headers = {'Client-ID': '<twitch-client-id>'}
    r = requests.get(url, headers=headers)

    try:
        json = r.json()
    except:
        return False

    if len(json['data']) > 0:
        return True
    else:
        return False


def startScraping(dir_name, channel):
    image_dir = os.listdir(dir_name)
    known_images = [fr.load_image_file(dir_name+'/'+i) for i in image_dir if i.endswith('.jpg')]
    known_encodings = []

    for image in known_images:
        temp = fr.face_encodings(image)
        if len(temp) > 0:
            known_encodings.append(temp[0])

    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless")

    filename = 'ss.jpg'
    link = "https://www.twitch.tv/" + channel
    if DEBUG:
        link = "https://www.twitch.tv/videos/556436677?t=2h48m20s"
    scrapFromTwitch(link, filename, chrome_options, channel, known_encodings)


while True:
    if isLive('lilypichu') or DEBUG:
        startScraping('michael', 'lilypichu')