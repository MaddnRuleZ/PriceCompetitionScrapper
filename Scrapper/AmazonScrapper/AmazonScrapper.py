import time
import re

from Scrapper.General import SelUtils
from Scrapper.General.GeneralScrapper import GeneralScrapper
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from selenium.webdriver.common.by import By
from Scrapper.ShoppifyScrapper.ScrapingResult import ScrapingResult

class AmazonScrapper(GeneralScrapper):

    def __init__(self, root_url, len, category):
        print("Amazon Scrapper Innit initialized")
        self.root = root_url
        super().__init__(self.root)
        self.category = category
        self.max_index = len

    def obtain_all_links(self):
        final_links = set()
        for x in range(1, self.max_index):
            final_links = final_links | self.get_all_links_current_site()
            self.navigate_next_site(x)

        for link in final_links:
            try:
                self.get_element(link)
            except:
                print("Error in link" + link)


    def get_element(self, url):
        self.driver.get(url)
        SelUtils.wait_random_time()
        name = ""
        price = ""
        desc = ""

        name = self.selNav.get_element(By.ID, "productTitle").text
        price = self.selNav.get_element(By.CSS_SELECTOR, "span.a-price-whole").text
        desc = self.get_product_desc()

        scrap = ScrapingResult(self.category, name, url, desc, price)
        scrap.add_to_database()

    def get_product_desc(self):
        try:
            # Find all <li> elements within the specified <ul> under the element with id "feature-bullets"
            list_items = self.driver.find_elements(By.CSS_SELECTOR,
                                                   'div#feature-bullets ul.a-unordered-list.a-vertical.a-spacing-mini > li')

            list_texts = []
            for li in list_items:
                list_texts.append(li.text.strip())
            all_text = '\n'.join(list_texts)

            return all_text
        except Exception as e:
            print("Error Obtaining Product Desc:", e)
            return None

    def navigate_next_site(self, index):
        print("navigating next Site")
        self.driver.get(self.replace_page_number(self.root, index))
        time.sleep(1)

    def replace_page_number(self, url, new_page_number):
        # Regular expression pattern to find and replace the page parameter
        pattern = r'(page=)\d+'

        # Replace the page number in the URL with the new page number
        new_url = re.sub(pattern, fr'\g<1>{new_page_number}', url)

        return new_url

    def get_all_links_current_site(self):
        link_elements = self.driver.find_elements(By.CSS_SELECTOR, "a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal")
        links = set()
        for element in link_elements:
            # Extract and return the href attribute value
            href = element.get_attribute("href")
            links.add(href)

        return links