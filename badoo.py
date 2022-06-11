from driverlib import *
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

f = open('descriptions.txt', 'a')
descriptions = []

try:
    driver_type, headless, profile_qty, username, password = load_config('settings.json', 'badoo')

    if driver_type == 'Firefox':
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")

        driver = webdriver.Firefox(options=options)

    elif driver_type == 'Chrome':
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--lang=en")
        options.add_argument('--window-size=1920x1080')

        driver = webdriver.Chrome(options=options)

    driver.get('https://badoo.com/signin/')

    smart_sleep_s(5)

    print('Logging in...')
    a = try_find_element_then_execute_action(find_element_by_placeholder, (driver, 'Email or phone number'), action = 'send_keys', action_params = username)
    a = try_find_element_then_execute_action(find_element_by_placeholder, (driver, 'Password'), action = 'send_keys', action_params = password)

    a = try_find_element_then_execute_action(find_element_by_class_name, (driver, 'checkbox-field__label'))
    a = try_find_element_then_execute_action(find_element_by_id, (driver, 'signin-submit'))

    print('Logging Sucessful!')

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
except Exception as e:
    print(e)
finally:
    print(descriptions)
    f.close()
    driver.quit()
