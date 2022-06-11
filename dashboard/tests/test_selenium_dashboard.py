from idna import valid_contextj
import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

@pytest.mark.selenium
def test_create_user(create_superuser):
    assert create_superuser.__str__() == "admin"

@pytest.mark.selenium
def test_dashboard_admin_login_page(live_server, create_superuser, chrome_browser_instance):
    browser = chrome_browser_instance

    browser.get(f"{live_server.url}/admin/login/")
    
    user_name = browser.find_element(By.NAME, value="username")
    password = browser.find_element(By.NAME, value="password")
    submit = browser.find_element(By.XPATH, '//input[@value="Log in"]')

    user_name.send_keys("admin")
    password.send_keys("password")
    submit.send_keys(Keys.RETURN)

    assert "Site administration" in browser.page_source