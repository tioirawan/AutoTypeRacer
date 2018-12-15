from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from dotenv import load_dotenv
from time import sleep
from os import getenv
from tabulate import tabulate

import sys
import pyautogui

# save each race result
history = []

# elements selector
signin_selector = '#tstats > table > tbody > tr.datarow > td:nth-child(1) > table > tbody > tr > td:nth-child(1) > a'
username_selector = 'body > div.DialogBox.trPopupDialog.editUserPopup > div > div > div.dialogContent > div > div.bodyWidgetHolder > div > table.gwt-DisclosurePanel.gwt-DisclosurePanel-open > tbody > tr:nth-child(2) > td > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > input'
password_selector = 'body > div.DialogBox.trPopupDialog.editUserPopup > div > div > div.dialogContent > div > div.bodyWidgetHolder > div > table.gwt-DisclosurePanel.gwt-DisclosurePanel-open > tbody > tr:nth-child(2) > td > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(1) > td > input'
signinconfirm_selector = 'body > div.DialogBox.trPopupDialog.editUserPopup > div > div > div.dialogContent > div > div.bodyWidgetHolder > div > table.gwt-DisclosurePanel.gwt-DisclosurePanel-open > tbody > tr:nth-child(2) > td > div > table > tbody > tr:nth-child(4) > td:nth-child(2) > table > tbody > tr > td:nth-child(1) > button'
play_selector = '#dUI > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > div.mainViewport > div > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(1) > td > a'

# just to check if the race page is loaded
banner_selector = 'body > div.countdownPopup.horizontalCountdownPopup > div > table > tbody > tr > td > table > tbody > tr > td:nth-child(2)'

# this selector needs #gwt-uid-{uid} >
text_selector = 'table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(1) > td > div > div'
input_selector = 'table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > input'
raceagain_selector = 'table > tbody > tr:nth-child(3) > td > table > tbody > tr > td:nth-child(2) > a'

# after race selector
wpm_selector = 'table > tbody > tr:nth-child(4) > td > div > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table > tbody > tr:nth-child(1) > td:nth-child(2) > table > tbody > tr > td:nth-child(1) > div > div'
time_selector = 'table > tbody > tr:nth-child(4) > td > div > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > span'
point_selector = 'table > tbody > tr:nth-child(4) > td > div > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table > tbody > tr:nth-child(4) > td:nth-child(2) > div > div'

# check if element exist using css selector
def isElementExist(selector):
    try:
        browser.find_element_by_css_selector(selector)
    except NoSuchElementException:
        return False
    return True

# get uid where race element nested
def bruteUID():
    print("bruteforce-ing uid...")
    uid = 0

    # try checking the input selector element
    while uid < 10000:
        input_selector = '#gwt-uid-%d > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > input' % uid
        if isElementExist(input_selector):
            break
        uid += 1

    print("uid found:", uid)

    return uid

# get text, input, and race-again element
def getRaceElementsSelector():
    uid = "#gwt-uid-%d > " % bruteUID()

    selectors = {
        'text': uid + text_selector, 
        'input': uid + input_selector, 
        'raceagain': uid + raceagain_selector,
        'wpm': uid + wpm_selector,
        'time': uid + time_selector,
        'point': uid + point_selector,
    }

    return selectors

# get and wait an element using css selector
def getAndWait(selector, key, max=60):
    print('get and wait:', key)
    return WebDriverWait(browser, max).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))

# find an element using css selector
def find(selector, key):
    print('find:', key)
    return browser.find_element_by_css_selector(selector)

def secureClick(element, key):
    while not element.is_displayed():
        print(key, 'is not visible, waiting for 1s')
        sleep(1)

    print('click:', key)
    element.send_keys(Keys.TAB)
    element.click()

# login using data from .env
def login():
    print("login...")
    getAndWait(signin_selector, 'sigin').click()
    getAndWait(username_selector, 'username').send_keys(getenv("username"))
    find(password_selector, 'password').send_keys(getenv("password"))
    find(signinconfirm_selector, 'signinconfirm').click()
    sleep(5)
    print("done login...")

# self explanatory
def race(count):
    try:
        #page loading check
        getAndWait(banner_selector,  'banner')

        selectors = getRaceElementsSelector()

        # select text element
        text = find(selectors['text'], 'text').text
        print("text:", text)
        # select text input element where we need to type the text
        text_input = find(selectors['input'], "input")
                                                            
        # wait for game to start
        while text_input.get_attribute('disabled'):
            print("wait the race to start for 1s...")
            sleep(1)
        
        # after countdown is done, click the element (47)
        text_input.click()

        # type using pyautogui because I dont know how to set the typing speed
        print("typing...")
        pyautogui.typewrite(text, interval=0.14)

        # save the result
        result = [
            text[:10] + '...' + text[-10:],            
            getAndWait(selectors['wpm'], 'wpm').text,
            getAndWait(selectors['time'], 'time').text,
            getAndWait(selectors['point'], 'point').text
        ]

        history.append(result)

        count -= 1

        if count:
            secureClick(find(selectors['raceagain'], "raceagain"), "raceagain")
            race(count)
    except TimeoutException:
        print('kelamaan')

if __name__ == "__main__":
    load_dotenv()

    count = 1
    guestMode = False

    if len(sys.argv) > 1:
        count = int(sys.argv[1])

    if len(sys.argv) > 2:
        if sys.argv[2] == "g":
            print('Start in guest mode...')
            gustMode = True
    
    # disable image load and idk what disk-cache-size used for
    prefs = {'profile.managed_default_content_settings.images':2, 'disk-cache-size': 4096}
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", prefs)

    browser = webdriver.Chrome(chrome_options=options)

    browser.get('https://play.typeracer.com/')

    if not guestMode:
        login()

    # click the "enter typing race button"
    getAndWait(play_selector, 'playbutton').click()

    # RACE!!!!
    race(count)

    print('\nRESULTS:')
    print(tabulate(history, headers=['text', 'speed', 'time', 'point'], showindex=True))

    wpms = [int(res[1].split()[0]) for res in history]
    points = sum([int(res[3]) for res in history])
    print('\nAVERAGE WPM:', sum(wpms) / len(wpms))
    print('TOTAL POINTS:', points)
    