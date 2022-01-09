from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


def main():
    with Chrome() as driver:
        driver.get('https://www.scrapethissite.com/pages/ajax-javascript/')        


if __name__ == '__main__':
    main()