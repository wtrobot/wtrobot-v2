import sys, os, json
import logging
from src import commmandParser


def logger_init(filename):
    logging.basicConfig(
        filename=filename,
        level=logging.INFO,
        format="%(levelname)s - %(asctime)s - %(filename)s - %(lineno)d - %(message)s",
    )

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(levelname)s - %(asctime)s - %(filename)s - %(lineno)d - %(message)s"
    )
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)
    # marker to denote new log starting
    logging.info("------------------new---------------------")


if __name__ == "__main__":

    config_file_name = "config.json"
    config = dict()
    count = 0
    try:
        with open(config_file_name) as fobj:
            config = json.load(fobj)
            count = len(config)
    except (OSError, json.decoder.JSONDecodeError):
        print("config file missing or incorrect, please provide following configurations...")

    if config is None or "script_filepath" not in config.keys():
        config["script_filepath"] = (
            input("Test script filename: test.yaml ? ") or "test.yaml"
        )

    if config is None or "browser" not in config.keys():
        config["browser"] = input("Which browser : firefox ? ") or "firefox"

    if config is None or "webdriver_path" not in config.keys():
        config["webdriver_path"] = (
            input("Selenium webdriver : ./selenium_drivers/geckodriver ? ")
            or "./selenium_drivers/geckodriver"
        )

    if config is None or "locale" not in config.keys():
        config["locale"] = input("Which browser locale : en_US ? ") or "en_US"

    if config is None or "log" not in config.keys():
        config["log"] = (
            input("WTRobot execution log file path : wtlog.log ? ") or "wtlog.log"
        )

    logger_init(config["log"])
    if not os.path.exists(config["script_filepath"]):
        logging.error("Invalid script file path")
        sys.exit(0)

    if not os.path.exists(config["webdriver_path"]):
        logging.error("Invalid webdriver file path")
        sys.exit(0)

    if count < len(config):
        with open(config_file_name, "w") as fobj:
            json.dump(config, fobj, indent=4)

    obj = commmandParser(config)