import json
import time
import os
import sys
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    with open(resource_path("example.json"), "r") as f:
        credentials = json.load(f)
        username = credentials["username"]
        password = credentials["password"]

    config = ConfigParser()
    config.read(resource_path("example.ini"))
    CHROME_DRIVER_PATH = config.get("chromedriver", "path")
    DURATION = config.getint("delay", "seconds")
    print(CHROME_DRIVER_PATH)
    
    driver = webdriver.Chrome(resource_path(CHROME_DRIVER_PATH))
    URL = config.get("website", "url")
    driver.get(URL)
    driver.find_element_by_xpath('//a[@href="/login"]').click()

    time.sleep(DURATION)
    username_form_input = driver.find_element_by_id("username")
    time.sleep(DURATION)
    username_form_input.send_keys(username)
    time.sleep(DURATION)

    password_form_input = driver.find_element_by_id("password")
    password_form_input.send_keys(password)
    password_form_input.send_keys(Keys.ENTER)
    time.sleep(DURATION)
    driver.close()


if __name__ == "__main__":
    main()