from typing import Type

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def webdriver_wait(driver: Type[WebDriver], timeout: int) -> WebDriverWait:
    return WebDriverWait(driver=driver, timeout=timeout)


def get_webelement_text(web_element: WebElement):
    return web_element.text


class NaminatedMoviesCrawler:
    def __init__(self) -> None:
        self.driver: Chrome = Chrome()
        
    def scrap(self):
        self.driver.get('https://www.scrapethissite.com/pages/ajax-javascript/')
        year_links: list = reversed(self.driver.find_elements(By.CLASS_NAME, 'year-link')) # type: ignore
        for year_link in year_links:
            year_link.click()
            movie_table = webdriver_wait(driver=self.driver, timeout=3).until(       # type: ignore
                EC.visibility_of_element_located((By.ID, 'table-body'))
            )
            for movie in movie_table.find_elements(By.CLASS_NAME, 'film'):
                movie_info_dict = {'year': get_webelement_text(web_element=year_link)}
                movie_info_dict['name'] = get_webelement_text(web_element=movie.find_element(By.CLASS_NAME, 'film-title'))
                movie_info_dict['film_nominations'] = get_webelement_text(web_element=movie.find_element(By.CLASS_NAME, 'film-nominations'))
                movie_info_dict['film_awards'] = get_webelement_text(web_element=movie.find_element(By.CLASS_NAME, 'film-awards'))
                print(movie_info_dict)
            
    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     self.driver.close()
    
    def __del__(self):
        self.driver.close()


if __name__ == '__main__':
    crawler: NaminatedMoviesCrawler = NaminatedMoviesCrawler()
    crawler.scrap()