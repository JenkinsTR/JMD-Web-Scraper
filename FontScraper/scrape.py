import os
import requests
import selenium
import time
import subprocess
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

# Set the path of ChromeDriver - relative to this py
DRIVER_PATH = 'chromedriver_107.exe'

# Set the master URI of the crawl
# This version of scape py is designed specifically for dafont.com font scraping
# accepts a single word term as the only argument, corresponding to the dafont.com page to scrape from
# e.g python scrape.py top
URI = f'https://www.dafont.com/{argv[1]}.php?page={argv[2]}&fpp=200'
# URI = f'https://google.com.au'

print(f"Scraping {URI} . . .")

# Set selenium options
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
list_links = driver.find_elements(By.CSS_SELECTOR, 'a.dl')

output_dir = os.path.join(os.getcwd(), argv[1])

# Make directory.
try:
    os.mkdir(output_dir)
    os.chdir(output_dir)
except FileExistsError:
    os.chdir(output_dir)

# Loop through links and download each one
for i in list_links:
    filename = i.get_attribute('href').split("/")
    fileurl = i.get_attribute('href').split("=")
    print(f"FileURL: https://dl.dafont.com/dl/{filename[-1]}")
    downloadlink = f"https://dl.dafont.com/dl/?f={fileurl[-1]}"
    filename = filename[-1][3:]
    print(f"Filename: {filename}")
    with open(f"{filename}.zip", "wb") as file:
        # get request
            response = requests.get(downloadlink)
            # write to file
            print(f"\u001b[33mDownloading {filename}.zip")
            file.write(response.content)
            print("\u001b[32;1mStatus Code:{}\nTime Elapsed:{} \u001b[0m".format(response.status_code,response.elapsed))
            # create new folder for each zip file
            ### folder_name = filename
            # Make directory.
            ### try:
            ###     os.mkdir(os.path.join(output_dir, folder_name))
            ### except FileExistsError:
            ###     pass
            ### print(f"\u001b[33mExtracting {filename}.zip \u001b[0m")
            # extract the zip file in the newly created folder
            ### time.sleep(1)
            ### subprocess.run(["7z", "x", "-o"+os.path.join(output_dir, folder_name), os.path.join(output_dir, f"{filename}.zip")])
            print()

# Quite selenium gracefully
driver.quit()