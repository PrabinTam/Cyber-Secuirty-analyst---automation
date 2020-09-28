#! /usr/bin/python3

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from get_vuln_list import init_driver

# The purpose of this scrip is to go to the Sophos console and download all the computers in the consolde

#Go to the Sophos console and log in with username and password
def lookup(driver, url):
    driver.get(url)
    username = 'yourusernmae'
    password = 'yourpassword'
    time.sleep(3)       # wait 3 seconds to load
    driver.find_element_by_xpath('//*[@id="signInName"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
    # click sign in
    driver.find_element_by_xpath('//*[@id="next"]').click()

    #asking for Duo code from the User
    security_code = input("security code: ")
    #Entering the Duo code
    driver.find_element_by_xpath('//*[@id="code"]').send_keys(security_code)
    #clicking okay after the duo
    driver.find_element_by_xpath('//*[@id="form"]/button').click()

# Download all the computers in a csv format
def sophos_download(driver):
    wait = WebDriverWait(driver, 20)
    driver.get("url of the download")
    time.sleep(5)
    #downloading the file
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#sc-button-bulk-computers-export-link'))).click()
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    #initialize the driver from the get_vuln_list.py, see get_vuln_list.py for specification of the browser
    driver = init_driver()
    website =lookup(driver, "url of the sophos")
    sophos_download(driver)

