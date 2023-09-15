"""Collection of functions used for retrieving the source code of a web page"""

__all__ = ['browser_open_source_page', 'save_source_page']

import asyncio

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from loguru import logger as LOGGER

import settings


async def browser_open_source_page():
    """Function to get page source"""

    options = Options()
    options.add_argument('--no-sandbox')  # to run as root on linux server
    driver = webdriver.Chrome(options=options)
    driver.get(settings.MAIN_LINK)
    await asyncio.sleep(10)
    driver.save_screenshot('screenshot.png')
    driver.get(f'view-source:{settings.MAIN_LINK}')
    await asyncio.sleep(10)
    page = driver.page_source
    await asyncio.sleep(3)

    await save_source_page(page)

    LOGGER.success('Driver has gotten source')
    driver.close()


async def save_source_page(page):
    """Saves downloaded page to file"""

    with open('source.html', 'w', encoding='utf-8') as output_file:
        output_file.write(page)
    LOGGER.success('source.html has been saved')
