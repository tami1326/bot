from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By


class BookingReport:
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def print_results(self):
        products = self.driver.find_elements(By. XPATH, './/div[@class="c066246e13"]')

        table = []
        for product in products:

            title_tag = product.find_element(By. CSS_SELECTOR, 'div[data-testid="title"')
            title = title_tag.text

            score_tag = product.find_element(By. CSS_SELECTOR, 'div[aria-label~="Scored"]')
            score = score_tag.text

            price_tag = product.find_element(By. CSS_SELECTOR, '*[data-testid="price-and-discounted-price"]')
            price = price_tag.text

            row = (title, score, price)
            table.append(row)
        return table