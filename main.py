import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

# Variables initialization
input_publ = input("What user's you'd like to scrap?(login): ")
input_follow = input("What you'd like to scrap: following(2) or followers(1), enter a number: ")
count_of_foll = int(input("Count of followings/followsers: "))
counter_sleep = 4
counter_scrolling = 600
counter_processed = 0


# Open browser and get the url
browser = webdriver.Firefox(executable_path='/home/alexandr/geckodriver')
browser.get('https://www.instagram.com/accounts/login/')
try:
    login = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, 'username'))
    )
except TimeoutException:
    browser.quit()
    sys.exit()
password = browser.find_element_by_name('password')

# Put your login and password
login.send_keys('hack___yourself')
password.send_keys("Hacker1109200")
password.send_keys(Keys.ENTER)

# If you have e-mail/phone verification put time.sleep(60) to have time to enter a code
time.sleep(40)
browser.get('https://www.instagram.com/' + input_publ)
time.sleep(4)
followers_label = browser.find_elements_by_class_name('-nal3')
followers_label[int(input_follow)].click()
time.sleep(3)
try:
    followers_label = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'isgrP'))
    )
except TimeoutException:
    browser.quit()


# Scraping followers/followings from account you choose and write them into a file
for _ in range(int(count_of_foll/9)):
    browser.execute_script("elem = document.getElementsByClassName('isgrP')[0]; elem.scroll(0,{0})".format(counter_scrolling))
    time.sleep(.7)
    counter_scrolling += 600
array_nicks = browser.find_elements_by_class_name('d7ByH')
file = open('file.txt', 'w')
for nick in array_nicks:
    file.write(nick.text + '\n')
file.close()
file_info_users = open('info_users.txt', 'w')
with open('file.txt', 'r') as f:
    logins = f.read().splitlines()

# Getting Instagram-API to find user_id and if there is public e-mail on account
# 200 requests per hour is maximum to not get blocked
for l in logins:
    if counter_sleep >= 200:
        time.sleep(3650)
        print('Waiting one hour...')
        counter_sleep = 3
    print('Processed {0} of {1}'.format(counter_processed, len(logins)))
    counter_processed += 1
    counter_sleep += 2
    browser.get('https://www.instagram.com/{0}/?__a=1'.format(l))
    page_src = browser.page_source
    user_id = re.search(r'profilePage_\d+', page_src)
    try:
        user_id = user_id.group(0).split('_')[1]
    except AttributeError:
        continue
    else:
        browser.get('https://i.instagram.com/api/v1/users/{0}/info/'.format(user_id))
        source = browser.page_source
        if not 'public_email' in source:
            continue
        temp_email = re.search(r'public_email": "\S+', source)
        temp_email = temp_email.group(0)
        if not '@' in temp_email:
            continue
        email = re.search(r' "\S+["]', temp_email)
        email = email.group(0).split('"')[1]
        username = re.search(r'"username": \S+"', source)
        username = username.group(0)
        file_info_users.write(email + '  ' + username.split('"')[3] + '\n\n')
        print(email + '  ' + username.split('"')[3] + '\n\n')

file_info_users.close()
browser.quit()