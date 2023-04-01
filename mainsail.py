import secure
import sys
import time
import config
from selenium.webdriver.common.by import By

# Selenium settings
driver = config.driver
default_implicit_wait = config.default_implicit_wait
wait_time = config.wait_time
driver.implicitly_wait(default_implicit_wait)


def home(module, menu_item, debug=False):

    menu_item = menu_item.lower()
    module = module.lower()

    element_text = ''
    found = False
    try:
        elements = driver.find_elements(By.CLASS_NAME, "menu-item")
    except:
        print('Selenium was unable to find the element class')
        driver.quit()
        sys.exit()

    match module:
        case 'tools':
            for element in elements:
                # remove numbers
                element_text = ''.join([i for i in element.text if not i.isdigit()])
                # remove line break
                element_text = element_text[1:]
                if element_text.lower() == menu_item:
                    menu_item = element
                    menu_item_text = element_text
                    found = True
                    break
        case 'reports':
            repeated = False
            for element in elements:
                # remove numbers
                element_text = ''.join([i for i in element.text if not i.isdigit()])
                # remove line break
                element_text = element_text[1:]
                if element_text.lower() == menu_item:
                    if repeated:
                        menu_item = element
                        break
                    if menu_item == 'billing':
                        repeated = True
                    menu_item = element
                    menu_item_text = element_text
                    found = True
        case 'create':
            for element in elements:
                # remove numbers
                element_text = ''.join([i for i in element.text if not i.isdigit()])
                # remove line break
                element_text = element_text[8:]
                if element_text.lower() == menu_item:
                    menu_item = element
                    menu_item_text = element_text
                    found = True
                    break
        case 'search':
            for element in elements:
                # remove numbers
                element_text = ''.join([i for i in element.text if not i.isdigit()])
                # remove line break
                element_text = element_text[2:]
                if element_text.lower() == menu_item:
                    menu_item = element
                    menu_item_text = element_text
                    found = True
                    break
        case 'show_all':
            i = 0
            for element in elements:
                # remove numbers
                #element_text = ''.join([i for i in element.text if not i.isdigit()])
                # remove line break
                #element_text = element_text[1:]
                print(i, ":", element.text)
                i = i + 1
            return
        case _:
            print('The module', module, 'was not found in this role/screen')
            driver.quit()
            sys.exit()

    if found:
        menu_item.click()
        print('Successful access to Mainsail', menu_item_text, 'screen')
        time.sleep(wait_time)
    else:
        print('The Menu Item', menu_item, 'was not found in this role/screen')
        driver.quit()
        sys.exit()
    return





