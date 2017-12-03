from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests as r
import pandas as pd
from bs4 import BeautifulSoup
import re
from time import sleep
from random import shuffle

class MN_State(object):
    def __init__(self):
        self.categories = [200,202,203,204,201,205,206,207,208,209,210,211,212,213]

        self.menu = {}
        self.url = "http://www.minnstate.edu/college-search/public/institution?delMode=%s&matchPercentage=0&award=&category=%i"
        self.url += "&subcategory=%i"
        self.url += "&zipCode=&zipCodeRadius=500&offset=0&numberOfResults=10&programView=true&activeTab=programSearch&pageNumber=%i"
        self.driver = webdriver.Chrome()
        self.start()

    def start(self):
        self.get_categories()
        for menu_item in self.menu.keys():
            for subcat in self.menu[menu_item]:
                for option in ['O','L']:
                    max_page_num = 1
                    page_num = 0
                    while page_num<max_page_num:
                        html_source, title_cat, title_subcat = self.get_page(menu_item, subcat, page_num+1, option)
                        self.save_page(html_source, title_cat, title_subcat, page_num+1, option)

                        max_page_num = self.get_max_page_num(html_source)
                        print(title_cat, title_subcat, option, page_num+1, 'max:', max_page_num)
                        page_num += 1


    def get_categories(self):
        for category in self.categories:
            response = r.get("http://www.minnstate.edu/college-search/public/institution?delMode=O&matchPercentage=0&award=&category=%i&subcategory=&zipCode=&zipCodeRadius=50&offset=0&numberOfResults=10&programView=true&activeTab=programSearch&pageNumber=1&keyword=&_=1512095651539" % category)

            soup = BeautifulSoup(response.content, "lxml")
            subcats = soup.find(id="programSubcategory")
            subcats = re.findall(r'[0-9][0-9][0-9]',str(subcats))
            self.menu[category] = subcats

    def get_max_page_num(self, html_source):
        page_numbers = re.findall(r'data-lp="[0-9]*"',html_source)

        if len(page_numbers):
            return int(page_numbers[-1:][0].split('"')[1].split('"')[0])
        else:
            return 1

    def get_page(self, menu_item, subcat, page_num, option):

        url = self.url % (option, int(menu_item), int(subcat), page_num)
        self.driver.get(url)
        sleep(.6)
        html_source = str(self.driver.page_source.encode())
        #self.driver.find_element_by_css_selector("input[type='radio'][value='L']").click()

        # get title of page
        selected = re.findall(r'"selected"[ ]*>[A-Za-z ,\/-]*<', html_source)
        category = selected[0].split('>')[1][:-1]
        if len(selected)>1:
            sub_category = selected[1].split('>')[1][:-1]
        else:
            sub_category = 'Main'
        return html_source, category, sub_category

    def save_page(self, html_source, menu_item, subcat, page_num, option):

        with open('./mn_state/%s_%s_%s_%s.html' % (menu_item, subcat.replace('/','#').replace(', ', '@'), option, page_num),'w') as f:
            f.write(str(html_source))
MN_State()
