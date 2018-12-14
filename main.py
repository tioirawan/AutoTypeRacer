from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from time import sleep

import pyautogui

prefs = {'profile.managed_default_content_settings.images':2, 'disk-cache-size': 4096}
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", prefs)

browser = webdriver.Chrome(chrome_options=options)

browser.get('https://play.typeracer.com/')

play_selector = '#dUI > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > div.mainViewport > div > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(1) > td > a'
text_selector = '#gwt-uid-15 > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(1) > td > div > div'
input_selector = '#gwt-uid-15 > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > input'

def getAndWait(selector):
    return WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))

def getText():
    text = getAndWait(text_selector).text
    print("Teks:", text)
    return text

# wait until the play button is ready

try:
    play_button = getAndWait(play_selector)
    play_button.click()
 
    sleep(3)
        
    text_input = getAndWait(input_selector)

    text = getText()
                                                          
    # wait for game to start
    while text_input.get_attribute('disabled'):
        print("still waiting for start...")
        sleep(1)
        
    text_input.click()

    print("typing...")
    pyautogui.typewrite(text, interval=0.15)
except TimeoutException:
    print('kelamaan')
