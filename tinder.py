from driverlib import *
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

f = open('descriptions.txt', 'a')
descriptions = []

try:
    driver_type, headless, profile_qty, username, password = load_config('settings.json', 'tinder_facebook')

    if driver_type == 'Firefox':
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.set_preference("geo.enabled", True)
        options.set_preference("geo.prompt.testing", True)
        options.set_preference("geo.prompt.testing.allow", True)

        driver = webdriver.Firefox(options=options)

    elif driver_type == 'Chrome':
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_experimental_option('prefs', {'geolocation': True})
        options.add_argument("--lang=en")
        options.add_argument('--window-size=1920x1080')

        driver = webdriver.Chrome(options=options)

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

except Exception as e:
    print(e)
finally:
    print(descriptions)
    f.close()
    driver.quit()