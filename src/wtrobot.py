import time
import logging
from src import Operations, ActionChains 

class WTRobot(Operations):

    def __init__(self, driver):
        self.driver = driver

    def logger_decorator(function):
        def logger_wrapper(*args):
            self = args[0]
            test_data = args[1]
            logging.info("TestCase:{} - Step:{} - {}".format(test_data["testcase_no"],test_data["step_no"], test_data["name"])) 
            function(*args)
            if "screenshot_name" not in test_data.keys():
                test_data["screenshot_name"] = int(round(time.time() * 1000))
            self.full_page_screenshot(test_data["screenshot_name"])
        return logger_wrapper

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
        except Exception as e:
            logging.error(e)


    @logger_decorator
    def click(self, test_data):
        try:
            click_obj = self.get_element(test_data["target"])
            click_obj.click()
            
            self.driver.switch_to_default_content()
        
        except Exception as e:
            logging.exception(e)
        # print(test_data)
    
    @logger_decorator
    def hover(self, test_data):
        hover_obj = self.get_element(test_data["target"])
        ActionChains(self.driver).move_to_element(hover_obj).perform()
        # print(test_data)

    @logger_decorator
    def input(self, test_data):
        try:
            input_obj = self.get_element(test_data["target"])
            input_obj.send_keys(test_data["value"])
        except Exception as e:
            logging.exception(e)
        # print(test_data)

    @logger_decorator
    def screenshot(self, test_data):
        if "screenshot_name" not in test_data.keys():
            test_data["screenshot_name"] = int(round(time.time() * 1000))
        self.full_page_screenshot(test_data["screenshot_name"])
    
    @logger_decorator
    def sleep(self, test_data):
        try:
            time.sleep(test_data["value"])
        except Exception as e:
            logging.exception(e)

    @logger_decorator
    def wait(self, test_data):
        print(test_data)
    
    @logger_decorator
    def validate(self, test_data):
        print(test_data)

    @logger_decorator
    def function(self, test_data):
        print(test_data)

    
    
# if __name__ == "__main__":
#     obj = WTRobot(None)
