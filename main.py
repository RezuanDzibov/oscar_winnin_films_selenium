from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class MainCrawler:
    def __init__(self) -> None:
        self.driver: Chrome = Chrome()
        
    def scrap(self):
        self.driver.get('https://www.scrapethissite.com/pages/ajax-javascript/')
        year_links = self.driver.find_elements(By.CLASS_NAME, 'year-link')
        for year_link in year_links:
            year_link.click()

    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     self.driver.close()
    
    def __del__(self):
        self.driver.close()


if __name__ == '__main__':
    crawler: MainCrawler = MainCrawler()
    crawler.scrap()