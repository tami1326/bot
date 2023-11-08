import time
import booking.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import datetime
import calendar

class Booking(webdriver.Chrome):
    def __init__(self, driver_path = r"\\drivers\\chromedriver-mac-x64\\chromedriver", teardown = False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(Booking, self).__init__()
        self.implicitly_wait(15)
        # self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def accept_cookies(self):
        accept_btn = self.find_element(By. ID, 'onetrust-accept-btn-handler').click()

    def close_campaign(self):
        try:
            WebDriverWait(self, 2).until(
                EC.presence_of_element_located((By. XPATH, './/button[@class="a83ed08757 c21c56c305 f38b6daa18 d691166b09 ab98298258 deab83296e f4552b6561"]'))
            )
            close_btn = self.find_element(By. XPATH, './/button[@class="a83ed08757 c21c56c305 f38b6daa18 d691166b09 ab98298258 deab83296e f4552b6561"]').click()
            print('Closed')
        except:
            print('No Campaign')

    def change_currency(self, currency):
        print(currency)
        currency_element = self.find_element(By. CSS_SELECTOR, 
        'button[data-testid="header-currency-picker-trigger"]')
        currency_element.click()

        selected_currency_element = self.find_element(By. XPATH, f'.//div[contains(text(), "{currency}")]')
        selected_currency_element.click()

    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(By. XPATH, 
        './/div[@class="hero-banner-searchbox"]//input')
        search_field.click()
        search_field.send_keys(place_to_go)
        print('waiting..')
        time.sleep(1)
        first_result = self.find_element(By. ID, 'autocomplete-result-0').click()


    def select_dates(self, check_in, check_out):
        check_in_month, check_in_month_name, check_in_day, check_in_year = Booking.parse_date(self, check_in)

        check_out_month, check_out_month_name, check_out_day, check_out_year = Booking.parse_date(self, check_out)

        Booking.select_date(self, check_in_month_name, check_in_year, check_in_day)

        Booking.select_date(self, check_out_month_name, check_out_year, check_out_day)


    def select_date(self, month_name, year, day):

        isDate = False

        while not isDate:
            current_month_tag = self.find_elements(By. XPATH, './/div[@class="d358556c65"]')
            
            for current_month_name in current_month_tag:
                if month_name in current_month_name.text and str(year) in current_month_name.text:
                    isDate = True 
                    select_day_tag = current_month_name.find_element(By. XPATH, f'.//*[contains(text(), "{str(day)}")]').click()
            check_next_month = self.find_element(By. XPATH, './/button[@class="a83ed08757 c21c56c305 f38b6daa18 d691166b09 f671049264 deab83296e f4552b6561 dc72a8413c f073249358"]').click()   


    def parse_date(self, date):

        date_parsed = datetime.strptime(date, '%Y-%m-%d')

        date_month = date_parsed.month

        month_name = calendar.month_name[date_month]

        day = date_parsed.day

        year = date_parsed.year

        return date_month, month_name, day, year

        
    

