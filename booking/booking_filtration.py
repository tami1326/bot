# Filter results from booking
import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

class BookingFiltration:
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def apply_star_rating(self, *stars):
        for star in stars:
            apply_filter = self.driver.find_element(By. CSS_SELECTOR, f'div[data-filters-item="class:class={star}"]').click()

    def sort_options(self):
        time.sleep(1)
        apply_filter = self.driver.find_element(By. CSS_SELECTOR, 'button[data-testid="sorters-dropdown-trigger"]').click()
        est_price_review = self.driver.find_element(By. CSS_SELECTOR, 'button[data-id="review_score_and_price"]').click()


    

