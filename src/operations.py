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
    
    def get_element_by_xpath_or_text(self, element_data):
        xpath_denoter = ("//","/html","/")
        
        if element_data.startswith(xpath_denoter):
            return WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, element_data)))
        else:
            xpath = "//*[contains(text(),'{0}') or contains(@value,'{0}')]".format(element_data)
            return WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
        
    def get_element_inside_iframe(self, test_data):
        try:
            # get all iframes 
            iframes = self.driver.find_elements_by_tag_name("iframe")
            #iterate through all iframes
            for iframe in range(len(iframes)):
                self.driver.switch_to_frame(iframe)
                logging.info("switching to iframe_no: {}".format(iframe))
                # locate our element
                try:
                    elem_obj = self.get_element_by_xpath_or_text(test_data["target"])
                    if elem_obj:
                        test_data["iframe_no"] = iframe
                        test_data["element_obj"] = elem_obj    
                except Exception:
                    self.driver.switch_to_default_content()
        except Exception as e:
            logging.error(e)

        return test_data


    def get_element(self, test_data):

        try:
            # if iframe_no is given then use it 
            # and if any exception occure again go through all iframe and locate element  
            if "iframe_no" in test_data.keys():
                try:
                    self.driver.switch_to_frame(test_data["iframe_no"])
                    logging.info("switching to iframe_no: {}".format(test_data["iframe_no"]))
                    elem_obj = self.get_element_by_xpath_or_text(test_data["target"])
                    if elem_obj:
                        test_data["element_obj"] = elem_obj
                except Exception:
                    print("element not found")
                    self.driver.switch_to_default_content()
                    test_data = self.get_element_inside_iframe(test_data)
            
            else:
                test_data["element_obj"] = self.get_element_by_xpath_or_text(test_data["target"])

        except ElementNotVisibleException:
            logging.exception("Element Not Visible Exception")

        except Exception:
            # if element is inside iframe then...
            test_data = self.get_element_inside_iframe(test_data)
        
        return test_data

    
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
