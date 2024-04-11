import random
import time
import re
from urllib.parse import urlparse, urljoin
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By

def wait_random_time(min=1, max=3):
    random_time = random.uniform(min, max)  # Generate a random float between 1 and 3
    time.sleep(random_time)

def get_links_with_keyword(driver, keyword, max_links=2):
        base_url = urlparse(driver.current_url).scheme + '://' + urlparse(driver.current_url).hostname

        all_links = driver.find_elements(By.TAG_NAME, 'a')
        matching_links = []
        retries = 1  # Number of retries

        for _ in range(retries):
            try:
                for link in all_links:
                    href = link.get_attribute('href')
                    if href:
                        full_url = urljoin(base_url, href)
                        if base_url in full_url and keyword in full_url:
                            matching_links.append(full_url)

                # If we found matching links, break out of the loop
                if matching_links:
                    break
            except StaleElementReferenceException:
                # If StaleElementReferenceException is raised, refresh the page
                driver.refresh()
                # Re-fetch all links after the page refresh
                all_links = driver.find_elements(By.TAG_NAME, 'a')
                continue

        return matching_links[:max_links]

def get_email_addresses(driver):
        # Get the page source
        page_source = driver.page_source
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+(?:\(at\)|@)[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        email_addresses = email_pattern.findall(page_source)
        return email_addresses