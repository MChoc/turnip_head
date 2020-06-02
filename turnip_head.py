import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from win10toast import ToastNotifier


class TurnipHead():
    def __init__(self):
        self.SLEEP_TIME = 2
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.CONFIG = self.startup()
        self.TURNIP_RUN = True

    def startup(self):
        with open(os.path.join(self.BASE_DIR, 'config.json')) as f:
            print("Loaded config")
            return json.load(f)

    def stop(self):
        self.TURNIP_RUN = False
        print(f"Turnip turned off")

    def run(self, debugging=False):
        self.startup()

        """Start monitoring animal crossing turnip site"""
        print("Starting scrape")

        history = {}

        while self.TURNIP_RUN:
            all_prices, prices = self.scrape_islands(history)
            self.remove_inactive(history, all_prices)
            self.send_notification(prices)
            if debugging:
                break
            print("Scrape loop complete")

        # for name, price in prices.items():
        #     driver = webdriver.Chrome()
        #     driver.get(CONFIG['islands_url'])
        #     time.sleep(SLEEP_TIME)

        #     all_islands = driver.find_element_by_xpath("//*[text()=' All Islands ']")
        #     all_islands.click()
        #     time.sleep(SLEEP_TIME)

        #     base = driver.find_element_by_id('app')
        #     host = base.find_element_by_xpath(f".//div/div/div/div/h2/p[contains(text(),' {name} ')]")
        #     host.click()
        #     time.sleep(SLEEP_TIME)

        #     time.sleep(1000)

    def scrape_islands(self, history):
        driver = webdriver.Chrome()
        driver.get(self.CONFIG['islands_url'])
        time.sleep(self.SLEEP_TIME)

        test = driver.find_element_by_xpath("//*[text()=' All Islands ']")
        test.click()
        time.sleep(self.SLEEP_TIME)

        prices = {}
        all_prices = {}
        for elem in driver.find_elements_by_css_selector('.note'):
            name = elem.find_element_by_xpath('.//div/h2/p').text
            price = int(elem.find_element_by_xpath('.//div/div/p').text.split()[0])
            if price > 500:
                all_prices[name] = price
                # Check against history
                if name not in history:
                    prices[name] = price
                    history[name] = price
                    break
                else:
                    continue
        
        driver.quit()

        return all_prices, prices

    def remove_inactive(self, history, all_prices):
        """Remove inactive islands"""

        delete = []
        for key in history.keys():
            if key not in all_prices:
                delete.append(key)

        for i in delete:
            del history[i]


    def send_notification(self, prices):
        """Send notifications windows"""

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


if __name__=="__main__":
    turnip = TurnipHead()
    turnip.run(debugging=False)
