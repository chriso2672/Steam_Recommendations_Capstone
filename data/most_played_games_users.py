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


def get_user_ids(url, max_games, max_reviews):
    game_ids = get_game_ids(url, max_games)
    all_user_ids = set()
    for game_id in game_ids:
        url = f"https://steamcommunity.com/app/{game_id}/reviews/?p=1&browsefilter=mostrecent"
        driver.get(url)        
        if driver.find_elements_by_xpath('/html/body/div[1]/div[7]/div[9]/div'):
            el = driver.find_elements_by_xpath('//*[@id="age_gate_btn_continue"]')[0]
            action = webdriver.common.action_chains.ActionChains(driver)
            action.move_to_element_with_offset(el, 5, 5)
            action.click()
            action.perform()
       
        last_position = driver.execute_script("return window.pageYOffset;")
        user_ids = set()
        while True:
            cards = driver.find_elements_by_class_name('apphub_Card')
            if(len(cards)>=max_reviews):
                break
            last_position = driver.execute_script("return window.pageYOffset;")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            curr_position = driver.execute_script("return window.pageYOffset;")
            if(last_position==curr_position):
                break
                
            for card in cards:
                profile_url = card.find_element_by_xpath('.//div[@class="apphub_friend_block"]/div/a[2]').get_attribute('href')
                user_id = profile_url.split('/')[-2]
                if user_id.isdigit():
                    user_ids.add(int(user_id))
        all_user_ids.update(user_ids)
    return all_user_ids

most_played = "https://steamdb.info/graph/"

most_played_user_ids = get_user_ids(most_played, '1K',  100)
driver.close()

# Store data (serialize)
with open('mpui.pickle', 'wb') as handle:
    pickle.dump(most_played_user_ids, handle, protocol=pickle.HIGHEST_PROTOCOL)

# # Load data (deserialize)
with open('mpui.pickle', 'rb') as handle:
    unserialized_mpui = pickle.load(handle)

print(unserialized_mpui, len(unserialized_mpui))
print("--- %s seconds ---" % (time.time() - start_time))