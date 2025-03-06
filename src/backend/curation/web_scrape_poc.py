from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()

browser.get('https://www.monroecc.edu/depts/testingservices/preparing-for-your-test/arithmetic-sample-questions/')
assert 'Monroe' in browser.title

elem = browser.find_element(By.NAME, 'p')  # Find the search box
elem.send_keys('seleniumhq' + Keys.RETURN)

browser.quit()