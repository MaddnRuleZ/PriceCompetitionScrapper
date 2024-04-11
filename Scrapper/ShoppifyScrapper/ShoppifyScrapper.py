import time

from Scrapper.General.GeneralScrapper import GeneralScrapper
from selenium.webdriver.common.by import By

from Scrapper.ShoppifyScrapper.ScrapingResult import ScrapingResult


class ShopifyScrapper(GeneralScrapper):

    def __init__(self, root_url, len, category):
        print("ShopifyScrapper Innit initialized")
        self.root = root_url
        super().__init__(self.root)
        self.category = category
        self.max_index = len
        # add all param in param

    def get_element(self, url):
        self.driver.get(url)
        time.sleep(1)
        name = ""
        price = ""
        desc = ""

        name = self.selNav.get_element(By.CSS_SELECTOR, "div.product__title > h1").text
        price = self.selNav.get_element(By.CSS_SELECTOR, "span.price-item.price-item--sale.price-item--last").text
        if not self.is_float(price):
            price = self.convert_price_to_float(price)
            if not self.is_float(price):
                print("Error Price " + str(price) + " is no float")
                return


        desc = self.get_product_desc()
        scrap = ScrapingResult(self.category, name, url, desc, price)
        scrap.add_to_database()

    def convert_price_to_float(self, price_string):
        try:
            # Convert price_string to a string if it's not already
            price_string = str(price_string)

            # Remove any non-numeric characters from the string
            price_string = price_string.replace(",", "").replace("EGP", "").strip()

            # Convert the cleaned string to float
            price_float = float(price_string)

            return price_float
        except ValueError:
            print("Error: Unable to convert price to float.")
            return None  # Returning None instead of price_string if conversion fails

    def get_product_desc(self):
        try:
            # Find all <span> elements within the specified <ul>
            span_elements = self.driver.find_elements(By.CSS_SELECTOR,
                'ul.a-unordered-list.a-vertical.a-spacing-mini span.a-list-item')

            # Initialize an empty string to store the concatenated text
            all_text = ""

            # Iterate over each <span> element and append its text to the all_text string
            for span in span_elements:
                all_text += span.text + "\n"

            return all_text
        except Exception as e:
            print("Error Obtaining Product Desc:", e)
            return None

    def obtain_all_links(self):
        final_links = set()
        for x in range(1, self.max_index):
            final_links = final_links | self.get_all_links_current_site()
            self.navigate_next_site(x)

        for link in final_links:
            self.get_element(link)


    def navigate_next_site(self, index):
        print("navigating next Site")
        self.driver.get(self.root + "?page=" + str(index))
        time.sleep(1)

    def get_all_links_current_site(self):
        link_elements = self.driver.find_elements(By.XPATH, "//li[contains(@class, 'grid__item')]//a")
        links = set()
        for element in link_elements:
            # Extract and return the href attribute value
            href = element.get_attribute("href")
            links.add(href)

        return links

    def is_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False


