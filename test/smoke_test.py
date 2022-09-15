import time

from src.base import SeleniumBase

selenium_base = SeleniumBase()
selenium_base.setup_driver()

selenium_base.driver.get('https://google.com')
selenium_base.click_and_send_key(
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input',
    'Python\n',
)
time.sleep(1)

assert selenium_base.driver.current_url.startswith(
    'https://www.google.com/search?q=Python'
)

selenium_base.driver.close()
