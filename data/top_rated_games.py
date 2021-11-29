from datetime import datetime 
import string
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen
import requests,json,os,sys,time,re
import pickle

start_time = time.time()

options = Options()
options.add_argument("--disable-notifications")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path='C:/bin/chromedriver', chrome_options=options)

def get_game_ids(url, amount):
    driver.get(url)
    show_dropdown={x.text : x for x in driver.find_elements_by_xpath('//*[@id="table-apps_length"]/label/select/option')}
    show_dropdown[amount].click()

    game_rows = driver.find_elements_by_tag_name('tr')
    game_ids = [x.get_attribute('data-appid') for x in game_rows][1:]
    return game_ids


url = "https://steamdb.info/stats/gameratings/"
top_rated_games = get_game_ids(url, '5K')


with open('top_rated_games.pickle', 'wb') as handle:
    pickle.dump(top_rated_games, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Load data (deserialize)
with open('top_rated_games.pickle', 'rb') as handle:
    tr = pickle.load(handle)

print(tr, len(tr))
print("--- %s seconds ---" % (time.time() - start_time))