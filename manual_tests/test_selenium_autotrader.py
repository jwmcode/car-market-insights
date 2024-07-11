import time
from selenium import webdriver
import os

p = os.getenv("PATH")
# Optional argument, if not specified will search path.
driver = webdriver.Chrome()
driver.get('https://www.autotrader.co.uk/used-cars')
time.sleep(10)  # Let the user actually see something!

# popup is in iframe. switch to it and accept all
driver.switch_to.frame("sp_message_iframe_252633")
element = driver.find_element_by_xpath('/html/body/div/div[3]/div[3]/div[2]/button[2]')
print(element)
element.click()

driver.switch_to.default_content()
element = driver.find_element_by_xpath(
    '/html/body/div[1]/main/article/section[1]/div/form/div[2]/div[2]/div[2]/div[1]/div/input')
print(element)
element.send_keys('NR22PP')
driver.quit()
