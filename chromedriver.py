from selenium.webdriver.chrome.options import Options
#import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

###Chromedriver init###
chrome_options = Options();chrome_service = Service()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=chrome_service,options=chrome_options)



