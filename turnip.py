# """Example 1"""
# toaster = ToastNotifier()
# toaster.show_toast(
#     "Hello World!!!",
#     "Python is 10 seconds awsm!",
#     icon_path="custom.ico",
#     duration=10
# )

# """Example 2"""
# toaster.show_toast(
#     "Example two",
#     "This notification is in it's own thread!",
#     icon_path=None,
#     duration=5,
#     threaded=True
# )
# # Wait for threaded notification to finish
# while toaster.notification_active(): time.sleep(0.1)

import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from win10toast import ToastNotifier

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, 'config.json')) as f:
    CONFIG = json.load(f)


def run():
    """Start monitoring animal crossing turnip site"""
    history = {}

    while True:
        # Grab islands page
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(CONFIG['islands_url'])
        time.sleep(1)

        prices = {}
        all_prices = {}
        for elem in driver.find_elements_by_css_selector('.note'):
            name = elem.find_element_by_xpath('.//div/h2').text
            price = int(elem.find_element_by_xpath('.//div/div/p').text.split()[0])
            if price > 500:
                all_prices[name] = price
                # Check against history
                if name not in history:
                    prices[name] = price
                    history[name] = price
                else:
                    continue
        
        # Remove entries in hist that didn't show up this time
        delete = []
        for key in history.keys():
            if key not in all_prices:
                delete.append(key)
        
        for i in delete:
            del history[i]
        
        # Send notification to windows
        toaster = ToastNotifier()
        str_prices = ""
        if prices:
            for i, (name, price) in enumerate(prices.items()):
                str_prices += "{} - {}\n".format(name, price)
                i =+ 1
                if i % 4 == 0:
                    print(i)
                    toaster.show_toast("Turnip Prices", str_prices, duration=5)
                    print(str_prices)
                    str_prices = ""
            toaster.show_toast("Turnip Prices", str_prices, duration=5)
            print(str_prices)
        else:
            str_prices = "No new islands"
            print(str_prices)

        # Run every minute
        driver.quit()
        time.sleep(10)


if __name__=="__main__":
    run()
