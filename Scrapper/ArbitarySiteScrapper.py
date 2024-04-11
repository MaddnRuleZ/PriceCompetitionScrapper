from Scrapper.General import SelUtils
from Scrapper.General.GeneralScrapper import GeneralScrapper

class ArbitarySiteScrapper(GeneralScrapper):
    def __init__(self, url):
        print("Arbitary Site Scrapper initialized")
        super().__init__(url)

        self.matching_links_set = set()
        self.emailAddresses = set()

    def get_matching_links(self):
        keywords = []
        keywords.append("impressum")
        keywords.append("kontakt")
        keywords.append("contact")
        keywords.append("services")
        emails = self.get_all_matching_links(keywords)

        print(emails)
        # todo add save logic, database . . .

        return emails

    def get_all_matching_links(self, keywords):
        print("Obtaining Matching Links")

        # Initialize dictionaries to store links for each keyword
        keyword_links = {keyword: [] for keyword in keywords}

        # Iterate through each keyword and fetch links
        for keyword in keywords:
            keyword_links[keyword] = SelUtils.get_links_with_keyword(self.driver, keyword)

        # Combine all links into a single set
        combined_set = set().union(*keyword_links.values())
        combined_set.add(self.url)

        # Iterate through each link, fetch email addresses, and add to set
        for url in combined_set:
            print("Fetching emails from:", url)
            self.driver.get(url)
            self.emailAddresses.update(SelUtils.get_email_addresses(self.driver))

        # Join email addresses into a single string
        email_addresses = ", ".join(email for email in self.emailAddresses)
        return email_addresses





