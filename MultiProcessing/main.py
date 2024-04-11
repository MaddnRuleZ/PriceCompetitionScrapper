import time

from MultiProcessing import MultiProcessing
from Scrapper.AmazonScrapper.AmazonScrapper import AmazonScrapper
from Scrapper.ShoppifyScrapper.ScrapingResult import ScrapingResult

from Scrapper.ShoppifyScrapper.ShoppifyScrapper import ShopifyScrapper
from Utilities import FileSystem, GeneralUtils


def test_multiproccessing():
    list = FileSystem.read_text_file("dox/ArbitarySiteScrapperTest/ArbitarySiteScrapper.txt")
    mul = MultiProcessing()
    mul.init_multiprocessing(list)

def test_ascii_art():
    total_steps = 100
    for i in range(total_steps + 1):
        progress = i / total_steps
        GeneralUtils.display_progress_bar(progress)
        time.sleep(0.1)  # Simulate some work being done
    print("\nTask completed!")


def test_cases():
    # excact duplicate URL
    src = ScrapingResult("baby", "Philips AVENT1 Microwave Steam Sterilizer", "google.com", "google.com", "1000")
    src.add_to_database()

    src = ScrapingResult("baby", "Philips AVENT2 Microwave Steam Sterilizer", "google1.com", "google.com", "1000")
    src.add_to_database()

    src = ScrapingResult("baby", "Philips AVENT Microwave Steam Sterilizer", "google.com" "idk", "google.com", "1000")
    src.add_to_database()

    src = ScrapingResult("baby", "Philips AVENT Microwave Steam Sterilizer", "google.com" "idk", "google.com", "1000")
    src.add_to_database()

    src = ScrapingResult("baby", "Philips AVENT Microwave Steam Sterilizer", "google.com" "idk", "google.com", "1000")
    src.add_to_database()

if __name__ == '__main__':

    '''
    
    am = AmazonScrapper("https://www.amazon.eg/-/en/s?k=philips+avent&i=baby&rh=n%3A18017931031%2Cn%3A21820644031&dc&page=1&language=en&crid=2HMG5NIPTKRWQ&qid=1712666264&rnid=18017931031&sprefix=philips+avent%2Cbaby%2C178&ref=sr_pg_2",
                        5, "baby")
    am.obtain_all_links()
    time.sleep(2)
    '''

    shop = ShopifyScrapper("https://babyblisseg.com/collections/baby-bottles", 3, "baby")
    shop.obtain_all_links()

    time.sleep(2)

    shop = ShopifyScrapper("https://babyblisseg.com/collections/baby-devices", 3, "baby")
    shop.obtain_all_links()


