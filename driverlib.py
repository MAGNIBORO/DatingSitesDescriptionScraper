from time import sleep
import json
import random
from selenium.webdriver.common.by import By

def load_config(filename, credentials_obj_name):
    cred_file = open(filename, 'r')
    data = json.load(cred_file)
    cred_file.close()

    driver_type = data['driver']
    headless = data['headless']
    profile_qty = data['profile_qty']
    username = data['credentials'][credentials_obj_name]['username']
    password = data['credentials'][credentials_obj_name]['password']

    return (driver_type, headless, profile_qty, username, password)

def smart_sleep(min, max):
    sleep(random.uniform(min, max))

def smart_sleep_s(seconds):
    smart_sleep(seconds, seconds+1)

def find_element_by_xpath(dvr, xpath):
    return dvr.find_element( by = By.XPATH, value= xpath)

def find_element_by_placeholder(dvr, placeholder):
    return dvr.find_element( by = By.XPATH, value= '//*[@placeholder="{}"]'.format(placeholder))

def find_element_by_class_name(dvr, class_name):
    return dvr.find_element( by = By.XPATH, value= '//*[@class="{}"]'.format(class_name))

def find_element_by_id(dvr, id):
    return dvr.find_element(by = By.ID, value= id)

def find_element_by_data_test_id(dvr, id):
    return dvr.find_element(by = By.XPATH, value= '//*[@data-testid="{}"]'.format(id))

def find_elements_by_data_test_id(dvr, id):
    return dvr.find_elements(by = By.XPATH, value= '//*[@data-testid="{}"]'.format(id))

def try_find_element(func, params, retries = 4):
    while retries >= 0:
        try:
            a = func(*params)
            return a
        except:
            smart_sleep(0.7, 1.3)
            retries -= 1
    return None

def try_find_element_then_execute_action(func, params, seconds = 5, action = 'click', action_params = None, sleep = 1):
    ret = try_find_element(func, params, seconds)
    
    try:
        if action == 'click':
            ret.click()
        elif action == 'send_keys':
            ret.send_keys(action_params)
    except:
        print('Cannot perform action {} on element {}'.format(action, params))
        pass

    smart_sleep(1, 1.3)

def send_keys_sleep(element, keys, seconds = 1):
    element.send_keys(keys)
    smart_sleep(seconds)