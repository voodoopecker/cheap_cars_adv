'''Collection of functions used for retrieving the source code of a web page'''

__all__ = ['browser_open_source_page', 'save_source_page', 'gui_browser_source_saving']

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import pyautogui
from loguru import logger as LOGGER

import settings

class NewChrome(uc.Chrome):
    '''New uc.Chrome class for preventing browser shutdown'''

    def __del__(self):
        pass


async def browser_open_source_page():
    '''Function to get page source'''

    # options = uc.ChromeOptions()
    # options.add_argument('--headless=new')
    # driver = NewChrome(use_subprocess=True, options=options)

    # driver = uc.Chrome(use_subprocess=True, options=options)

    options = Options()
    # options.headless = True
    driver = webdriver.Chrome(options=options)

    driver.get(settings.MAIN_LINK)
    time.sleep(10)
    driver.save_screenshot('screenshot.png')
    driver.get(f'view-source:{settings.MAIN_LINK}')
    time.sleep(10)
    page = driver.page_source
    time.sleep(3)

    await save_source_page(page)

    LOGGER.success('Driver has gotten source')
    driver.close()


async def save_source_page(page):
    '''Saves downloaded page to file'''

    with open('source.html', 'w', encoding='utf-8') as output_file:
        output_file.write(page)
    LOGGER.success('source.html has been saved')


async def gui_browser_source_saving():
    '''Browser GUI algorithm for working with websites that have protection against automated scraping'''

    pyautogui.hotkey('ctrl', 's')  # open save as dialog
    time.sleep(3)
    pyautogui.press('enter')
    time.sleep(3)
    pyautogui.hotkey('ctrl', 'j')  # open downloads page
    time.sleep(3)
    pyautogui.click(x=841, y=403)  # press stop
    time.sleep(3)
    pyautogui.click(x=752, y=348)  # press retry
    time.sleep(5)
    pyautogui.hotkey('alt', 'f4')
    time.sleep(1)
