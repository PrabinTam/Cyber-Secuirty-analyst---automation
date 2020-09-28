#!/usr/bin/env python3

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

# initialize the selenium browser.
def init_driver():
    # Setting up the Chrome.
	chrome_options = Options()
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-gpu')    # This will run Chrome without chrome being visible to us
	chrome_options.add_argument('--headless')
    # Specifying the Download folder
	prefs = {'download.default_directory': '/root/Desktop/project/vuln'}
	chrome_options.add_experimental_option('prefs', prefs)
	capabilities = DesiredCapabilities.CHROME.copy()
	capabilities['acceptSslCerts'] = True
	capabilities['acceptInsecureCerts'] = True
#	chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path
	driver = webdriver.Chrome(desired_capabilities=capabilities, chrome_options=chrome_options)
	driver.maximize_window()
	return driver

# Go to the url and retun the wait function of selenium
def lookup(driver, url):
	driver.get(url)
	wait = WebDriverWait(driver, 30)
	return wait

# log in to Tenable.
def login(driver, wait):
	wait.until(EC.visibility_of_element_located((By.ID, 'username'))).send_keys('yourusername')
	wait.until(EC.visibility_of_element_located((By.ID, 'password'))).send_keys('yourpassword')
	driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/section/form/input[2]').click()	#click sign in
	time.sleep(3)

# Download the Vulnerabilities
def download(driver, wait):
	#export as csv
	driver.execute_script("arguments[0].click();", driver.find_element_by_css_selector('.export-csv'))
	driver.execute_script("arguments[0].click();", driver.find_element_by_css_selector('a#form-overlay-submit.btn.btn-primary.mr'))
	time.sleep(3)
	driver.quit()

if __name__ == "__main__":
	driver = init_driver()
	wait = lookup(driver, "url of the tenable)
	login(driver, wait)
	download(driver,wait)
