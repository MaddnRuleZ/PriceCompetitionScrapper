from selenium.webdriver.common.by import By


class SelNav:

    def __init__(self, driver):
        self.driver = driver

    # todo add get Functions as Utilities with Exec handeling
    def get_element(self, selector, value):
        """
        Finds an element using the given selector and value.

        Parameters:
            - selector: The selector strategy (By) to use.
                        Options: By.CSS_SELECTOR, By.CLASS_NAME, By.ID
            - value: The value of the selector.

        Returns:
            - The WebElement if found, else None.
        """
        try:
            element = self.driver.find_element(selector, value)
            return element
        except Exception as e:
            print(f"Failed to find element using {selector}: {value}. Error: {e}")
            return None

    def get_elements(self, selector, value):
        """
        Finds an element using the given selector and value.

        Parameters:
            - selector: The selector strategy (By) to use.
                        Options: By.CSS_SELECTOR, By.CLASS_NAME, By.ID
            - value: The value of the selector.

        Returns:
            - The WebElement if found, else None.
        """
        try:
            elements = self.driver.find_elements(selector, value)
            return elements
        except Exception as e:
            print(f"Failed to find element using {selector}: {value}. Error: {e}")
            return None

    def get_href_from_element(self, element_xpath):
        """
        Retrieves the href attribute from a given element identified by its XPath.

        Args:
            driver (selenium.webdriver): The Selenium WebDriver instance.
            element_xpath (str): XPath of the element whose href attribute needs to be retrieved.

        Returns:
            str: The value of the href attribute, or None if the element is not found.
        """
        try:
            element = driver.find_element(By.XPATH, element_xpath)
            href = element.get_attribute("href")
            return href
        except Exception as e:
            print(f"Error: {e}")
            return None




    def send_text_to_element(self, element, text):
        try:
            element.clear()  # Clear any existing text in the element
            element.send_keys(text)  # Send text to the element
            print("Sended Text to Element " + text)
        except Exception as e:
            print(f"An error occurred while sending text to the element: {e}")

    def send_key(self, element, key):
        try:
            # Send the "END" key to the target element
            element.send_keys(key)
            print("Sent Key successfully.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
