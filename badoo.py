from time import sleep
import random
import json
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

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


cred_file = open('settings.json', 'r')
data = json.load(cred_file)
username = data['badoo']['username']
password = data['badoo']['password']
profile_qty = data['badoo']['profile_qty']
headless = data['badoo']['headless']
cred_file.close()


options = Options()
if headless:
    options.add_argument("--headless")


driver = webdriver.Firefox(options=options)
driver.get('https://badoo.com/signin/')

smart_sleep_s(5)

print('Logging in...')

a = try_find_element_then_execute_action(find_element_by_placeholder, (driver, 'Email or phone number'), action = 'send_keys', action_params = username)
a = try_find_element_then_execute_action(find_element_by_placeholder, (driver, 'Password'), action = 'send_keys', action_params = password)

a = try_find_element_then_execute_action(find_element_by_class_name, (driver, 'checkbox-field__label'))
a = try_find_element_then_execute_action(find_element_by_id, (driver, 'signin-submit'))

print('Logging Sucessful!')


descriptions = []
f = open('descriptions.txt', 'a')
prev_text = ''
text = ''

for i in range(profile_qty):
    a = try_find_element(find_element_by_class_name, (driver, "profile-section__content"), 10)
    try:
        text = str(a.text.encode('ascii', 'ignore'))
        if (prev_text != text):
            descriptions.append(text)
            f.write('\n' + text)
            prev_text = text
            print(text)
    except:
        pass

    ActionChains(driver).move_by_offset( 1, 1).perform()
    a = try_find_element_then_execute_action(find_element_by_class_name, (driver, "encounters-actions__item encounters-actions__item--yes"))
    a = try_find_element_then_execute_action(find_element_by_class_name, (driver, "btn btn--monochrome js-chrome-pushes-deny"), seconds = 0)


print(descriptions)
f.close()
