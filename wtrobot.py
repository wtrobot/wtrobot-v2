import argparse
import sys, os
import logging
from src import commmandParser

def logger_init(filename):
    logging.basicConfig(
        filename=filename, 
        level=logging.INFO,
        format="%(levelname)s - %(asctime)s - %(filename)s - %(lineno)d - %(message)s"
    )
    
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(filename)s - %(lineno)d - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)
    # marker to denote new log starting
    logging.info("------------------new---------------------")


if __name__ == "__main__":
    
    parser =argparse.ArgumentParser(description="WTRobot webautomation framework..")
    parser.add_argument("-s", "--script", metavar="", required=True, help="Testscript file path")
    parser.add_argument("-l", "--locale", metavar="", default="en_US",help="The language code to traverse in eg: en_US, ja_JP")
    parser.add_argument("-b", "--browser", metavar="", default="firefox", help="Browser to be used firefox/chrome")
    parser.add_argument("-d", "--driver", metavar="", help="File path to selenium webdriver eg: geckodriver, chromedriver.\
        By default it will firefox drivers from selenium_drivers dir locally")
    parser.add_argument("-L", "--log", metavar="", default="./wtlog.log", help="WTRobot execution log file path")

    args = parser.parse_args()
    logger_init(args.log)

    if not os.path.exists(args.script):
        logging.error("Invalid script file path")
        sys.exit(0)
    
    if args.browser and args.browser not in ["chrome","firefox"]:
        logging.error("Support browsers are only firefox and chrome")
        sys.exit(0)

    if args.driver and not os.path.exists(args.driver):
        logging.error("Invalid webdriver path")
        sys.exit(0)

    global_conf = {
        "script_filepath":args.script, 
        "locale":args.locale, 
        "browser":args.browser, 
        "webdriver_path":args.driver
    }
    
    obj = commmandParser(global_conf)
