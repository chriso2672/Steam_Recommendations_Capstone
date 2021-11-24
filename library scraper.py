from datetime import datetime 
import string
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen
import requests,json,os,sys,time,re
import pickle

start_time = time.time()

options = Options()
options.add_argument("--disable-notifications")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path='C:/bin/chromedriver', chrome_options=options)


id = '76561198023414915'

url = 'https://www.steamdiscovery.com/calculator.php'

member_since_public = '/html/body/div[3]/div[1]/div[1]/div/div[2]/div'
member_since_private = '/html/body/div[3]/div[1]/div[1]/div/div[2]/div'

def get_library(url, id):
    driver.get(url)
    search_box = driver.find_element_by_xpath('//*[@id="q"]')
    search_box.send_keys(str(id))
    search_box.submit()

    game_rows = driver.find_elements_by_tag_name('tr')
    # game_hours = [game_rows.find_elements_by_tag_name('td')[:2]  for game_row in game_rows]
    game_name_hours = []
    for row in game_rows:
        cells = row.find_elements_by_tag_name('td')[:2]
        cell_data = []
        for cell in cells:
            cell_data.append(cell.getAttribute("innerHTML"))
        print(cell_data)
        game_name_hours.append((cell_data[0], cell_data[1]))
    driver.close()
    return game_name_hours


print(get_library(url, id))