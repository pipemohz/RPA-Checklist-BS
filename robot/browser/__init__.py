import logging
from .events import *
from .web_driver import WebDriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from settings import CHROME_DRIVER_PATH
from robot import PATH


# Service instance for pointing to executable path of Chrome
service = Service(executable_path=CHROME_DRIVER_PATH)
# Browser options
chrome_options = webdriver.ChromeOptions()
prefs = {"download.default_directory": PATH}
chrome_options.add_experimental_option("prefs", prefs)


def browsing_session():
    logging.info("Browsing session started.")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    with WebDriver(driver) as d:
        login(d)
        select_report(d)
        set_exporting_filters(d)
        export_report(d, path=PATH)

    logging.info("Browsing session finished.")
