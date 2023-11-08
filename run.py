from booking.booking import Booking

with Booking() as bot:
    bot.land_first_page()
    bot.accept_cookies()
    # bot.change_currency(currency='USD')   
    bot.close_campaign()
    bot.select_place_to_go(place_to_go='New York')
    bot.select_dates(check_in='2024-01-24', check_out='2024-02-07')