from Utilities.Database import Database
import re

class ScrapingResult:

    def __init__(self, category, name, url, description, price):
        # Replace double quotes and single quotes with space in each string attribute
        self.category = category.replace('"', ' ').replace("'", ' ')
        self.name = name.replace('"', ' ').replace("'", ' ')
        self.url = url.replace('"', ' ').replace("'", ' ')
        self.description = description.replace('"', ' ').replace("'", ' ')
        self.price = price

    def add_to_database(self):
        try:
            msql = Database()
            msql.insert_scrape_result(self.category, self.name, self.price, self.description, self.url)
        except Exception as e:
            print("Fatal Error in " + self.name + "ERROR:", e)

    def remove_non_ascii(self, input_string):
        # Use regular expression to match all non-ASCII characters
        non_ascii_pattern = re.compile(r'[^\x00-\x7F]+')

        # Replace all non-ASCII characters with an empty string
        cleaned_string = non_ascii_pattern.sub('', input_string)

        return cleaned_string