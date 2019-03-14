import logging
import requests
from src import WebDriverWait, EC, By
import time

class Operations(object):
    
    def __init__ (self, driver):
        self.driver = driver
    
    def check_url(self, url):
        """
        This function is used to check if the given link is broken or not.It simply makes a http call and checks response
        :param url: link which you want to check
        :return: True if response is 200 else False
        """
        try:
            request = requests.get(url, verify=False)
            if request.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
    
    def get_element(self, element_data):
        try:
            return WebDriverWait(self.driver, 3000).until(
                    EC.presence_of_element_located((By.XPATH, element_data)))
        except Exception:
            logging.error("Element not found")

    def full_page_screenshot(self, image_name=None):
        try:
            if not image_name:
                image_name = int(round(time.time() * 1000))
            self.driver.get_screenshot_as_file("./tmp/{}.png".format(image_name))
        except Exception as e:
            logging.exception(e)
    