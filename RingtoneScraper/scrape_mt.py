import os
import sys
import requests
import selenium
import concurrent.futures
import time
from sys import argv

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


from time import sleep
uri_list = []
def Niggers(uri):
    filename = uri.split("/")
    fileurl = uri.split("-")
    downloadlink = f"https://mobcup.net/d/{fileurl[-1]}/mp3"
    with open(f"{filename[-1]}.mp3", "wb") as file:
        # get request
            response = requests.get(downloadlink)
            # write to file
            print(f"\u001b[33mDownloading {filename[-1]}.mp3")
            file.write(response.content)
            print("\u001b[32;1mStatus Code:{}\nTime Elapsed:{} \u001b[0m".format(response.status_code,response.elapsed))
DRIVER_PATH = 'chromedriver_107.exe'
URI = f'https://mobcup.net/search?q={argv[1]}&type=ringtone'
# URI = f'https://google.com.au'

print(f"Scraping {URI} . . .")

options = Options()
options.headless = True
options.add_argument("start-maximized")
options.add_argument('--log-level=3')

# Deprecated
# driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(URI)

time.sleep(2)  # Allow 2 seconds for the web page to open
scroll_pause_time = 1 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web

i = 1

while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break

# list_links = driver.find_elements(By.TAG_NAME, "a")

list_links = driver.find_elements(By.CSS_SELECTOR, 'a.title')

os.mkdir(f"{argv[1]}") 
os.chdir(f"{argv[1]}")

for i in list_links:
    uri_list.append(i.get_attribute('href'))
    
with concurrent.futures.ThreadPoolExecutor(max_workers=24) as executor:
    try:
        future_to_url = {executor.submit(Niggers, url.strip()): url for url in uri_list}
    except Exception as E:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        pass
driver.quit()