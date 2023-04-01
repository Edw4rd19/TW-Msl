from selenium import webdriver


# SELENIUM------------------------------------
driver_path = 'C:\chromedriver.exe'
driver = webdriver.Chrome(driver_path)
default_implicit_wait = 40
wait_time = 10
driver.implicitly_wait(default_implicit_wait)

# ENVIRONMENT---------------------------------
terminal = 'PCT'
environment = 'ALPHA'
input_type = 'M'
# EQUIPMENT-----------------------------------
default_trucker = 'SHPO'

default_eq_line = 'COS'
default_chs_type = 'OWN'
default_chs_line = 'COS'
default_eq_sizetype = '40DH'
default_ch_sizetype = '40CH'
# SEARCH-------------------------------------
default_search_method = 'API'
default_service_order = 'Booking'



