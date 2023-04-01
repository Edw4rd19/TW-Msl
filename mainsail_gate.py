import sys
import time
import config
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from env_setup import tst_dat_prep as tdp

# Selenium settings
driver = config.driver
default_implicit_wait = config.default_implicit_wait
wait_time = config.wait_time
driver.implicitly_wait(default_implicit_wait)

gate_transaction = ''

ctr_line = config.default_eq_line
ctr_size_type = config.default_eq_sizetype
ctr_search_method = config.default_search_method

ch_type = config.default_chs_type
ch_line = config.default_chs_line
ch_size_type = config.default_ch_sizetype
ch_search_method = config.default_search_method

tkr = config.default_trucker
tkr_search_method = config.default_search_method


def select_transaction(option):

    global gate_transaction
    gate_transaction=option

    found = False
    option = option.lower()
    try:
        elements = driver.find_elements(By.CLASS_NAME, "field")
    except:
        print('Selenium was unable to find the element class')
        driver.quit()
        sys.exit()

    # i = 0
    for element in elements:
        # remove numbers
        element_text = ''.join([i for i in element.text if not i.isdigit()])
        # remove line break
        element_text = element_text[1:]
        # display all list -> print(i, ":", element_text)
        # i = i + 1
        if element_text.lower() == option:
            found = True
            # select gate tx
            element.click()

            try:
                truck_license_field = driver.find_element(By.CLASS_NAME, "uppercase")
                truck_license_field.click()
            except:
                print('Truck license field not available or class changed')
                driver.quit()
                sys.exit()

            print(element_text, 'selected at Mainsail Gate screen')
            break

    if not found:
        print('The gate transaction:', option, 'was not found in this role/screen')
        driver.quit()
        sys.exit()


def line_popup(lane_id='dev'):
    print('Mainsail - Gate: Selecting ', lane_id, 'lane')
    try:
        lane_id_field = driver.find_element(By.ID, "react-select-3-input")
        lane_id_field.send_keys(lane_id)
        lane_id_field.send_keys(Keys.ENTER)
        time.sleep(1)
        try:
            lane_id_field.send_keys(Keys.ENTER)
        except:
            pass
        time.sleep(5)

    except:
        print('Error Lane ID field not present or not valid locator')
        driver.quit()
        sys.exit()
    print("Mainsail - Gate: Lane ID", lane_id, 'selected')


def read_transaction_form(info='mandatory'):
    try:
        elements = driver.find_elements(By.CLASS_NAME, "field")
    except:
        print('Error with required elements locator')
        driver.quit()
        sys.exit()
    if info.lower() == 'mandatory':
        i = 0
        # request = [element.text for element in elements]
        request = ['' for element in elements]
        driver.implicitly_wait(0)
        for element in elements:
            try:
                element.find_element(By.CLASS_NAME, 'asterisk')
                # print(i, element.text)
                if element.text.startswith('Tru'):
                    request[i] = ''
                else:
                    request[i] = element.text
            except:
                pass
            i = i + 1
    else:
        request = [element.text for element in elements]

    driver.implicitly_wait(default_implicit_wait)
    print('Screen info:', request)
    return request


def fill_trucker_data(request='test'):

    match request.lower():
        case 'test':
            truck_license = '1111111'
        case 'api':
            # ['full in', 'code']
            a = ['COS', 'CTR', '40CH']
            # ['TRK','SHPO']
            request_data('Trucker')
        case _:
            print("No trucker algorithm for", request, "input")

    try:
        elements = driver.find_elements(By.CLASS_NAME, "field")
        for element in elements:
            if element.text == 'Truck License':
                input_field = element.find_element(By.CLASS_NAME, 'uppercase')
                input_field.send_keys(truck_license)
                print("Truck license", truck_license, "entered")
    except:
        print("Error interacting with truck license field")
        sys.exit()
    try:
        button = driver.find_element(By.CLASS_NAME, "primary")
        button.click()
    except:
        print("Error interacting with continue button")


# a = ['CTR','full in', 'COS', '40CH']
def request_data(requested_data):

    results = [info for info in requested_data]
    i = 0

    for data in requested_data:
        match data.lower():

            case '':
                results[i] = ''

            case 'chassis':
                if ch_type.lower() == 'own':
                    results[i] = 'OWN'
                else:
                    match ch_search_method.lower():
                        case 'api':
                            print('Requesting', data, 'from', ch_search_method)
                            send = ['CHS', gate_transaction, ch_line, ch_size_type]
                            print('Sending to API --> ', send)
                            exec = tdp.run()
                            exec.run(send)
                            results[i] = exec.req_data_out[0]

            case 'container':
                match ctr_search_method.lower():
                    case 'api':
                        print('Requesting', data, 'from', ctr_search_method)
                        send = ['CTR', gate_transaction, ctr_line, ctr_size_type]
                        print('Sending to API --> ', send)
                        exec = tdp.run()
                        exec.run(send)
                        results[i] = exec.req_data_out[0]

            case 'trucker':
                pass
            case 'booking':
                results[i] = 'IM-A-BOOKING'
            case _:
                if data.startswith('Seal'):
                    results[i] = 'IM-A-SEAL'
                elif data.startswith('Booking'):
                    pass
                else:
                    print('No search script available for', data)

        i = i + 1

    return results


def generate_seal_number():
    seal_number = '123456'
    return seal_number


def fill_data(res):
    print(res)
    pass


# FOR MODDING DATA FROM MAIN

# ['CTR','full in', 'COS', '40CH']
def mod_container_line(line):
    global ctr_line
    ctr_line = line


def mod_container_size_type(size_type):
    global ctr_size_type
    ctr_size_type = size_type


def mod_container_search_method(search_method, value=''):
    global ctr_search_method
    ctr_search_method = search_method + value


def line_chassis(value=True):
    global ch_type
    ch_type = 'line'


def mod_chassis_line(line):
    global ch_line
    ch_line = line


def mod_chassis_size_type(size_type):
    global ch_size_type
    ch_size_type = size_type


def mod_chassis_search_method(search_method, value=''):
    global ch_search_method
    ch_search_method = search_method + value


def mod_trucker(trucker):
    global tkr
    tkr = trucker


def mod_trucker_search_method(search_method, value=''):
    global tkr_search_method
    tkr_search_method = search_method + value




