import time
import logging
from src import Operations, ActionChains, webdriver, WebDriverWait, EC, By 
from selenium.common.exceptions import ElementNotInteractableException, ElementNotVisibleException

class Actions(Operations):

    def __init__(self, global_conf):
        self.global_conf = global_conf
        self.browser_init()

    def logger_decorator(function):

        def logger_wrapper(*args):
            self = args[0]
            test_data = args[1]

            # If no name key in step then add none to avoid execption
            if "name" not in test_data.keys(): 
                test_data["name"] = None

            logging.info("TestCase:{} - Step:{} - {}".format(test_data["testcase_no"],test_data["step_no"], test_data["name"])) 
            
            # If sleep key mentioned in steps
            if "sleep" in test_data.keys():
                logging.info("Sleep for {} seconds before {} ".format(test_data["sleep"], test_data["action"]))
                time.sleep(test_data["sleep"])
            
            # If wait before action mentioned in steps
            elif "wait before action" in test_data.keys():
                logging.info("waiting before action")
                self.wait(test_data["wait before action"])

            #method call
            test_result_data = function(*args)
            
            # If wait before action mentioned in steps
            if "wait after action" in test_data.keys():
                logging.info("waiting after action")
                self.wait(test_data["wait after action"])

            # screenshot after every action
            screenshot_file_name = None
            if "screenshot_name" not in test_data.keys():
                screenshot_file_name = "{}_{}_{}_{}".format(test_data["testcase_no"],test_data["step_no"],self.global_conf["locale"], str(int(round(time.time() * 1000))))
            else:
                screenshot_file_name = "{}_{}".format(self.global_conf["locale"], test_data["screenshot_name"])
            self.full_page_screenshot(screenshot_file_name)
            
            return test_result_data
        
        return logger_wrapper


    def browser_init(self):
        '''
        init all selenium browser session and create driver object
        '''
        if not self.global_conf["webdriver_path"] and self.global_conf["browser"] == "firefox":
            self.global_conf["webdriver_path"] = "./selenium_drivers/geckodriver"
        elif  not self.global_conf["webdriver_path"] and self.global_conf["browser"] == "chrome":
            self.global_conf["webdriver_path"] = "./selenium_drivers/chromedriver"
        
        if self.global_conf["browser"] == "firefox":
            profile = webdriver.FirefoxProfile()
            profile.set_preference("intl.accept_languages", self.global_conf["locale"])
            profile.accept_untrusted_certs = True
            self.driver = webdriver.Firefox(firefox_profile=profile, executable_path=self.global_conf["webdriver_path"])
        elif self.global_conf["browser"] =="chrome":
            options = webdriver.ChromeOptions()
            options.add_experimental_option('prefs', {'intl.accept_languages': '{}'.format(self.global_conf["locale"])})
            self.driver = webdriver.Chrome(executable_path=self.global_conf["webdriver_path"], chrome_options=options)

        self.driver.maximize_window()


    @logger_decorator
    def goto(self, test_data):
        """
        This function will visit the URL specified
        :param test_data:
        :return: None
        """
        try:
            if test_data["target"]:
                if self.check_url(test_data["target"]):
                    self.driver.get(test_data["target"])
                else:
                    logging.error("Target URL not specified/invalid")
            else:
                logging.error("Target URL not specified/invalid")
                test_data["error"] = True
        except Exception as e:
            logging.error(e)
            test_data["error"] = True
        return test_data

    @logger_decorator
    def click(self, test_data):
        try:
            test_data = self.get_element(test_data)
            test_data["element_obj"].click()

            self.driver.switch_to_default_content()
        except ElementNotVisibleException:
            click_obj = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, test_data["target"])))
            ActionChains(self.driver).move_to_element(click_obj).perform()
        except ElementNotInteractableException:
            click_obj = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, test_data["target"])))
            ActionChains(self.driver).move_to_element(click_obj).perform()
        except:
            logging.exception("error")
            test_data["error"] = True

        return test_data
    
    @logger_decorator
    def hover(self, test_data):
        try:
            test_data = self.get_element(test_data)
            ActionChains(self.driver).move_to_element(test_data["element_obj"]).perform()
        except Exception as e:
            logging.exception(e)
            test_data["error"] = True
        
        return test_data

    @logger_decorator
    def input(self, test_data):
        try:
            test_data = self.get_element(test_data)
            test_data["element_obj"].send_keys(test_data["value"])
        except Exception as e:
            logging.exception(e)
            test_data["error"] = True

        return test_data

    @logger_decorator
    def screenshot(self, test_data):
        try:
            screenshot_file_name = None
            if "screenshot_name" not in test_data.keys():
                screenshot_file_name = "{}_{}_{}_{}".format(test_data["testcase_no"],test_data["step_no"],self.global_conf["locale"], str(int(round(time.time() * 1000))))
            else:
                screenshot_file_name = "{}_{}".format(self.global_conf["locale"], test_data["screenshot_name"])

            self.full_page_screenshot(screenshot_file_name)
        except Exception as e:
            logging.exception(e)
            test_data["error"] = True
        
        return test_data

    @logger_decorator
    def sleep(self, test_data):
        try:
            time.sleep(test_data["value"])
        except Exception as e:
            logging.exception(e)
            test_data["error"] = True
        return test_data

    @logger_decorator
    def validate(self, test_data):
        
        xpath_denoter = ("//","/html","/")

        if test_data["target"].startswith(xpath_denoter):
            try:
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, test_data["target"])))
            except:
                logging.error("Element not found")
                test_data["error"] = True
        else:
            try: 
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), '{}')]".format(test_data["target"]))))
            except:
                logging.error("Element not found")
                test_data["error"] = True

        return test_data

    @logger_decorator
    def function(self, test_data):
        print("yet to implement")
        return test_data
    
    
    def closebrowser(self, test_data):
        try:
            logging.info("Closing browser...")
            self.driver.close()
        except Exception as e:
            logging.exception(e)
        return test_data
