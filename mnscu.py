
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests as r
import pandas as pd
from bs4 import BeautifulSoup
import re
from time import sleep


driver = webdriver.Chrome()
driver.get('https://webproc.mnscu.edu/registration/search/advanced.html?campusid=mnonline')

#<input type="submit" value="Search >" class="btn-primary" title="Search" style="margin-left: 10em;" />
main_page_source = driver.page_source
#print(re.findall(r'<input type="radio"[A-Za-z=" _\/()]* \/>', main_page_source))
open_values = driver.find_elements_by_css_selector("input[type='radio'][name='openValue']")
delivery_values = driver.find_elements_by_css_selector("input[type='radio'][name='delivery']")
for open_value in open_values:
    for delivery_value in delivery_values:
        open_value.click()
        input()
        delivery_value.click()
        input()
        
        driver.find_element_by_css_selector("input[type='submit'][title='Search']").click()
        #<a id="yui-pg0-1-next-link" href="#" class="yui-pg-next">next &gt;</a>

        # iterate through all pages
        driver.find_element_by_css_selector("a[class='yui-pg-next']").click()

        html_source = str(driver.page_source)
        with open('./mnscu/%s.html' % ('out'),'w') as f:
            f.write(str(html_source))


        driver.get('https://webproc.mnscu.edu/registration/search/advanced.html?campusid=mnonline')
