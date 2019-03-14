from selenium import webdriver
import src 

if __name__ == "__main__":
    
    # driver = webdriver.Firefox(executable_path="./selenium_drivers/geckodriver")
    driver = webdriver.Chrome(executable_path="./selenium_drivers/chromedriver")
    driver.maximize_window()
    obj = src.commmandParser(driver= driver, script_filepath="test.yml")