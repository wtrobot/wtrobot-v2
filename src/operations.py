import logging
import requests
from src import WebDriverWait, EC, By
import time
import lxml.etree
from src import StringIO
from selenium.common.exceptions import ElementNotVisibleException

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
            return WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, element_data)))
        
        except ElementNotVisibleException:
            logging.exception("Element Not Visible Exception")

        except Exception as e:
            # if element is inside iframe then...
            try:
                # get all iframes 
                iframes = self.driver.find_elements_by_tag_name("iframe")
                #iterate through all iframes
                for iframe in range(len(iframes)):
                    self.driver.switch_to_frame(iframe)
                    logging.info("switching to iframe_no: {}".format(iframe))
                    # locate our element
                    try:
                        return WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element_data)))
                    
                    except Exception:
                        self.driver.switch_to_default_content()
            
            except Exception as e:
                logging.error(e)

    def full_page_screenshot(self, image_name=None):
        try:
            if not image_name:
                image_name = int(round(time.time() * 1000))
            self.driver.get_screenshot_as_file("./tmp/{}.png".format(image_name))
        except Exception as e:
            logging.exception(e)
    
    def wait(self, test_data):
        '''
        This method will wait for specified time/element/text on screen
        '''
        xpath_denoter = ("//","/html","/")

        if isinstance(test_data, int):
            time.sleep(test_data)
        
        elif test_data.startswith(xpath_denoter):
            try:
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, test_data)))
            except:
                logging.error("Element not found")
        else:
            try: 
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), '{}')]".format(test_data))))
            except:
                logging.error("Element not found")
