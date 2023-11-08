import time
import booking.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport
import os
from datetime import datetime
import calendar
from prettytable import PrettyTable

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
        except:
            print('No Campaign')


    def change_currency(self, currency):
        currency_element = self.find_element(By. CSS_SELECTOR, 
        'button[data-testid="header-currency-picker-trigger"]')
        currency_element.click()

        selected_currency_element = self.find_element(By. XPATH, f'.//div[contains(text(), "{currency}")]')
        selected_currency_element.click()


    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(By. XPATH, 
        './/div[@class="hero-banner-searchbox"]//input')
        search_field.click()
        time.sleep(1.0)
        search_field.send_keys(place_to_go)
        time.sleep(1)
        first_result = self.find_element(By. ID, 'autocomplete-result-0').click()


    def select_dates(self, check_in, check_out):
        check_in_month, check_in_month_name, check_in_day, check_in_year = Booking.parse_date(self, check_in)

        check_out_month, check_out_month_name, check_out_day, check_out_year = Booking.parse_date(self, check_out)

        Booking.check_date(self, check_in_month_name, check_in_year, check_in_day)

        Booking.check_date(self, check_out_month_name, check_out_year, check_out_day)


    def check_date(self, month_name, year, day):

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


    def add_occupants(self, section, number):

        all_sections = self.find_elements(By. XPATH, f'.//div[@class="bfb38641b0"]')

        for idx, num in enumerate(all_sections):

            if idx == section:

                increase_button = self.find_element(By. XPATH, f'.//div[@class="a7a72174b8"][{idx+1}]//div[@class="bfb38641b0"]//button[2]')

                decrease_button = self.find_element(By. XPATH, f'.//div[@class="a7a72174b8"][{idx+1}]//div[@class="bfb38641b0"]//button[1]')

                while number != int(num.text):

                    if number > int(num.text):
                        increase_button.click()
                    elif number < int(num.text):
                        decrease_button.click()


    def select_occupants(self, adults, children, rooms):
        open_modal = self.find_element(By. XPATH, './/button[@class="a83ed08757 ebbedaf8ac ada2387af8"]').click()

        Booking.add_occupants(self, 0, adults)
        Booking.add_occupants(self, 1, children)
        Booking.add_occupants(self, 2, rooms)

    
    def search(self):
        search_btn = self.find_element(By. XPATH, './/button[@class="a83ed08757 c21c56c305 a4c1805887 f671049264 d2529514af c082d89982 cceeb8986b"]').click()


    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(3, 4, 5)
        filtration.sort_options()
    
    def reports(self):
        time.sleep(2)
        report = BookingReport(driver=self)
        report.print_results()
        table = PrettyTable(
            field_names = ["Hotel Name", "Hotel Score", "Hotel Price"]
        )
        table.add_rows(report.print_results())
        print(table)