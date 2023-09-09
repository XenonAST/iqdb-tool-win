import sys
import os
import tempfile
import requests
import webbrowser
from time import sleep
import win32api
# import cv2 as cv


def iqdb_img(img_path, interval=0):
    print(f'Processing [{img_path}]', end='\t')

    if os.path.splitext(img_path)[-1].lower() not in ['.jpg', '.png', '.jpeg']:
        # win32api.MessageBox(0, f'[{img_path}] is not an img', 'Not allowed')
        print('Not an img!')
        return

    # path of browser
    CHROME_PATH = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

    # image augmentation

    files = {'file': open(img_path, 'rb')}
    res = requests.post('https://iqdb.org/', files=files)
    html = res.text

    # with open('before_html.html', 'w') as f:
    #     f.write(html)

    html = html.replace('<a href=\"//', '<a href=\"https://')
    html = html.replace('<img src=\'/', '<img src=\'https://iqdb.org/')
    html = html.replace('<img alt=\"icon\" src=\"/',
                        '<img alt=\"icon\" src=\"https://iqdb.org/')

    # with open('after_html.html', 'w') as f:
    #     f.write(html)

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".html", encoding='utf8') as f:
        f.write(html)
        webbrowser.get(CHROME_PATH).open_new_tab(f.name)

    print('...Done')

    sleep(interval)

if len(sys.argv) != 2:
    sys.exit('argv error!')

if os.path.isdir(sys.argv[1]):
    img_dir = sys.argv[1]
    subs = list(os.walk(img_dir))
    first_layer = subs[0]
    for i, obj in enumerate(first_layer[-1]):
        print(obj)
        img_path = os.path.join(img_dir, obj)
        iqdb_img(img_path, 5)
        print(f'[{i + 1}/{len(first_layer[-1])}] out', obj)
else:
    img_path = sys.argv[1]
    iqdb_img(img_path)
    sys.exit()
