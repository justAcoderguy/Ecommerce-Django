import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


@pytest.fixture(scope="module")
def chrome_browser_instance():
    """
    Create a Chrome browser instance and returns it
    """
    options = Options()
    options.headless = False
    driver = webdriver.Chrome(f"{str(BASE_DIR)}" + "/chromedriver", options=options)
    yield driver
    driver.quit()
