import csv
from typing import List, Optional, Type

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


class NominatedMoviesCrawler:
    def __init__(self, csv_filename: str = None) -> None:
        csv_filename = self.get_csv_filename(csv_filename=csv_filename)
        self.driver: WebDriver = Chrome()
        field_names = ['year', 'name', 'film_nominations', 'film_awards']
        self.csvfile = open(f'{csv_filename}', 'w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.csvfile, fieldnames=field_names)
        self.writer.writeheader()
        
    def scrap(self) -> None:
        self.nominated_movies: List[dict] = list()
        self.driver.get('https://www.scrapethissite.com/pages/ajax-javascript/')
        year_links: list = reversed(self.driver.find_elements(By.CLASS_NAME, 'year-link'))
        for year_link in year_links:
            year_link.click()
            self.scrap_year_movies(year_link=year_link)
        self.write_to_csv(data=self.nominated_movies)
                
    def scrap_year_movies(self, year_link: WebElement) -> None:
        movie_table: WebElement = webdriver_wait(driver=self.driver, timeout=3).until(
            EC.visibility_of_element_located((By.ID, 'table-body'))
        )
        for movie in movie_table.find_elements(By.CLASS_NAME, 'film'):
            movie_info_dict: dict = {'year': get_webelement_text(web_element=year_link)}
            self.scrap_movie(movie=movie, movie_info_dict=movie_info_dict)
            self.nominated_movies.append(movie_info_dict)
                
    def scrap_movie(self, movie: WebElement, movie_info_dict: dict) -> None:
        movie_info_dict['name'] = get_webelement_text(web_element=movie.find_element(By.CLASS_NAME, 'film-title'))
        movie_info_dict['film_nominations'] = get_webelement_text(web_element=movie.find_element(By.CLASS_NAME, 'film-nominations'))
        movie_info_dict['film_awards'] = get_webelement_text(web_element=movie.find_element(By.CLASS_NAME, 'film-awards'))
        
    def write_to_csv(self, data: List[dict]):
        self.writer.writerows(data)
    
    def get_csv_filename(self, csv_filename: Optional[str]) -> str:
        """[summary]
            Check if csv_filename was provided.
            
        Args:
            csv_filename (Optional[str]): 

        Returns:
            str: csv_filename
        """
        if csv_filename:
            if csv_filename.endswith('.csv'):
                return csv_filename
            else:
                return f'{csv_filename}.csv'
        else:
            return 'nominated_movies.csv'
    
    def __del__(self):
        self.driver.close()
        self.csvfile.close()