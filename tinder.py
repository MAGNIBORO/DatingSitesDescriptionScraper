from time import sleep
import random
import json
from selenium import webdriver
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
username = data['tinder_facebook']['username']
password = data['tinder_facebook']['password']
profile_qty = data['tinder_facebook']['profile_qty']
headless = data['tinder_facebook']['headless']
cred_file.close()


options = Options()
if headless:
    options.add_argument("--headless")

options.set_preference("geo.enabled", True)
options.set_preference("geo.prompt.testing", True)
options.set_preference("geo.prompt.testing.allow", True)


driver = webdriver.Firefox(options=options)
driver.get('https://tinder.com/')

smart_sleep_s(5)

print('Logging in...')

a = try_find_element_then_execute_action(find_element_by_data_test_id, (driver, "privacyPreferencesDecline"))
a = try_find_element_then_execute_action(find_element_by_data_test_id, (driver, "appLoginBtn"))
a = try_find_element_then_execute_action(find_element_by_data_test_id, (driver, "login"))

smart_sleep_s(2)

print('Facebook logging...')

tinder_window = driver.window_handles[0]
facebook_login_window = driver.window_handles[1]

driver.switch_to.window(facebook_login_window)

a = try_find_element_then_execute_action(find_element_by_id, (driver, "email"), action = 'send_keys', action_params = username)
a = try_find_element_then_execute_action(find_element_by_id, (driver, "pass"), action = 'send_keys', action_params = password)
a = try_find_element_then_execute_action(find_element_by_id, (driver, "loginbutton"))

driver.switch_to.window(tinder_window)

print('Logging Sucessful!')

a = try_find_element_then_execute_action(find_element_by_data_test_id, (driver, "allow"))
a = try_find_element_then_execute_action(find_element_by_data_test_id, (driver, "decline"))


descriptions = []
f = open('descriptions.txt', 'a')
prev_texts = []
texts = []

for i in range(profile_qty):
    a = try_find_element(find_elements_by_data_test_id, (driver, "recCard_info"))

    for i, element in enumerate(a):
        texts.append(str(element.text.encode('ascii', 'ignore')))
    
    for i, text in enumerate(texts):
        if text in prev_texts:
            continue

        descriptions.append(text)
        f.write('\n' + text)
        print(text)

    prev_texts = texts
    texts = []
    a = try_find_element_then_execute_action(find_element_by_data_test_id, (driver, "close"), seconds = 0)
    a = try_find_element_then_execute_action(find_element_by_data_test_id, (driver, "gamepadLike"))


print(descriptions)
f.close()