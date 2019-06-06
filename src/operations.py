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
            if "file:" in url:
                return True
            else: 
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
        
        try:
            if element_data.startswith(xpath_denoter):
                return WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, element_data)))
            else:
                xpath = "//*[contains(text(),'{0}') or contains(@value,'{0}')]".format(element_data)
                return WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
        except Exception:
            return None

    def get_element_inside_iframe(self, test_data, iframes = None):
        try:
            # get all iframes 
            if not iframes:
                iframes = self.driver.find_elements_by_tag_name("iframe")
            logging.info("iframes found: {0}".format(len(iframes)))
            
            #iterate through all iframes
            for iframe in range(len(iframes)):
                self.driver.switch_to_default_content()
                self.driver.switch_to_frame(iframe)
                logging.info("switching to iframe no: {0}".format(iframe))
                # locate our element
                try:
                    elem_obj = self.get_element_by_xpath_or_text(test_data["target"])
                    # if element found 
                    if elem_obj:
                        test_data["iframe no"] = iframe
                        test_data["element_obj"] = elem_obj
                    
                        # insert the valid xpath on 0th index of targets list
                        tmp_key = test_data["targets"].index(test_data["target"])
                        tmp_value = test_data["targets"].pop(tmp_key)
                        test_data["targets"].insert(0,tmp_value)
                        break
                    else:
                        # element not found but invalid iframe no exist then remove it 
                        if "iframe no" in test_data.keys():
                            test_data.pop("iframe no")
                        test_data["element_obj"] = None
                except Exception:
                    self.driver.switch_to_default_content()
        except Exception as e:
            logging.error(e)
            # iframe not found but invalid iframe no exist then remove it
            if "iframe no" in test_data.keys():
                test_data.pop("iframe no")
            test_data["element_obj"] = None
        return test_data


    def get_element(self, test_data):
        
        test_data["element_obj"] = None

        for locator_target in test_data["targets"]:
            # Till element not found iterate through target list
            if not test_data["element_obj"]:
                test_data["target"] = locator_target
                logging.info("finding element using locator: {0}".format(locator_target))
                try:
                    # if iframe no is given then use it 
                    # and if any exception occure again go through all iframe and locate element  
                    if "iframe no" in test_data.keys():
                        try:
                            self.driver.switch_to_frame(test_data["iframe no"])
                            logging.info("switching to iframe no: {0}".format(test_data["iframe no"]))
                            elem_obj = self.get_element_by_xpath_or_text(test_data["target"])
                            test_data["element_obj"] = elem_obj
                        except Exception:
                            print("element not found")
                            self.driver.switch_to_default_content()
                            test_data = self.get_element_inside_iframe(test_data)
                    
                    else:
                        self.driver.switch_to_default_content()
                        test_data["element_obj"] = self.get_element_by_xpath_or_text(test_data["target"])
                        iframes = self.driver.find_elements_by_tag_name("iframe")
                        # if no element obj found then check for iframes on page if yes then check elements if exisit in iframes  
                        if not test_data["element_obj"] and len(iframes) > 0:
                            logging.info("element not found so switching to iframes")
                            test_data = self.get_element_inside_iframe(test_data=test_data, iframes=iframes)

                except ElementNotVisibleException:
                    logging.exception("Element Not Visible Exception")
                    test_data["element_obj"] = None

                except Exception:
                    # if element is inside iframe then...
                    iframes = self.driver.find_elements_by_tag_name("iframe")
                    if len(iframes) > 0:
                        logging.info("element not found so switching to iframes")
                        test_data = self.get_element_inside_iframe(test_data=test_data)
                
                # insert the valid xpath on 0th index of targets list
                tmp_key = test_data["targets"].index(test_data["target"])
                tmp_value = test_data["targets"].pop(tmp_key)
                test_data["targets"].insert(0,tmp_value)

            else:
                break

        return test_data

    
    def full_page_screenshot(self, image_name=None):
        try:
            if not image_name:
                image_name = int(round(time.time() * 1000))
            self.driver.get_screenshot_as_file("./tmp/{0}.png".format(image_name))
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
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), '{0}')]".format(test_data))))
            except:
                logging.error("Element not found")
