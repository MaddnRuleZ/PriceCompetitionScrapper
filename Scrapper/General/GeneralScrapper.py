from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Scrapper.General import SelUtils
from Scrapper.General.SelNav import SelNav
from Utilities.Database import Database


class GeneralScrapper:

    def __init__(self, url):
        print("Innit Driver")
        self.url = url
        # HEADLESS OPTION
        chrome_options = Options()

        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1800, 900)

        # Set page load timeout value in seconds
        page_load_timeout = 30
        # Set script timeout value in seconds
        script_timeout = 30

        # Set page load timeout and script timeout
        self.driver.set_page_load_timeout(page_load_timeout)
        self.driver.set_script_timeout(script_timeout)
        # self.init_datbase()
        self.selNav = SelNav(self.driver)

        try:
            self.driver.get(url)
            SelUtils.wait_random_time()

        except Exception as e:
            print("Error occurred while loading the page: QUITTING DRIVER", e)
            self.driver.quit()
            raise

    def init_datbase(self):
        self.db = Database()

