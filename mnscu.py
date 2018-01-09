from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from time import sleep

driver = webdriver.Chrome()
driver.get('https://webproc.mnscu.edu/registration/search/advanced.html?campusid=mnonline')

main_page_source = driver.page_source

college_actual_values = driver.find_element_by_name("searchrcid").find_elements_by_tag_name('option')
college_value = college_actual_values[1]
college_value.click()
semester_actual_values = driver.find_element_by_name("yrtr").find_elements_by_tag_name('option')
subject_actual_values = driver.find_element_by_name('subject').find_elements_by_tag_name('option')
open_values = driver.find_elements_by_css_selector("input[type='radio'][name='openValue']")
delivery_values = driver.find_elements_by_css_selector("input[type='radio'][name='delivery']")


for college_value_index in range(1, len(college_actual_values)):
    driver.get('https://webproc.mnscu.edu/registration/search/advanced.html?campusid=mnonline')

    college_actual_values = driver.find_element_by_name("searchrcid").find_elements_by_tag_name('option')

    college_value = college_actual_values[college_value_index]
    college_value.click()

    semester_actual_values = driver.find_element_by_name("yrtr").find_elements_by_tag_name('option')

    for semester_value_index in range(len(semester_actual_values)):
        for subject_value_index in range(1, len(subject_actual_values)): #len(subject_actual_values)
            for open_value_index in range(len(open_values)):
                for delivery_value_index in range(1,len(delivery_values)):

                    driver.get('https://webproc.mnscu.edu/registration/search/advanced.html?campusid=mnonline')

                    college_actual_values = driver.find_element_by_name("searchrcid").find_elements_by_tag_name('option')

                    college_value = college_actual_values[college_value_index]
                    college_value.click()

                    semester_actual_values = driver.find_element_by_name("yrtr").find_elements_by_tag_name('option')

                    subject_actual_values = driver.find_element_by_name('subject').find_elements_by_tag_name('option')

                    open_values = driver.find_elements_by_css_selector("input[type='radio'][name='openValue']")
                    delivery_values = driver.find_elements_by_css_selector("input[type='radio'][name='delivery']")

                    semester_value = semester_actual_values[semester_value_index]

                    subject_value = subject_actual_values[subject_value_index]

                    open_value = open_values[open_value_index]
                    delivery_value = delivery_values[delivery_value_index]

                    college = college_value.text
                    semester = semester_value.text
                    subject = subject_value.text
                    openclosed = open_value.get_attribute('title')
                    delivery = delivery_value.get_attribute('title')
                    filename = college  + "_" + semester + "_" + subject + "_" + openclosed + "_" + delivery
                    filename = re.sub(r'\s+', '', filename)
                    filename = filename.replace('/','-')
                    print(filename.replace('(','').replace(')', ''))

                    semester_value.click()
                    subject_value.click()
                    if 'No courses' in driver.page_source:
                        continue

                    open_value.click()
                    delivery_value.click()

                    driver.find_element_by_css_selector("input[type='submit'][title='Search']").click()


                    # iterate through all pages
                    page_num = 0
                    while True:
                        print('writing', filename)
                        html_source = str(driver.page_source)
                        filename = filename+'_'+str(page_num)
                        with open('./mnscu/%s.html' % (filename.replace('(','').replace(')', '')),'w') as f:
                            f.write(str(html_source))

                        try:
                            driver.find_element_by_css_selector("a[class='yui-pg-next']").click()
                            page_num += 1
                        except:
                            break
