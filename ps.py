import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains


#user input
'''username = input('Enter your username:')
password = input('Enter your password: ')
grade = input('Enter the grade you want to update: ')
path = input('Copy the path of the excel sheet you want to update including file type suffix: ')'''

browser = webdriver.Chrome(executable_path='C:\Chromedriver\chromedriver.exe')
type(browser)
browser.get('https://eschool.smcisd.net/eSchoolPLUS/Account/LogOn')
browser.maximize_window()

#navigate through the site pages to reach student names
logElem = browser.find_element_by_id('UserName')
logElem.send_keys('tanya.rhodes')
passwordElem = browser.find_element_by_id('Password')
passwordElem.send_keys('ashley2018coun')
passwordElem.submit()
okElem = browser.find_element_by_id('setEnvOkButton')
okElem.click()
menuElem = browser.find_element_by_id('MainMenu')
menuElem.click()
schedElem = browser.find_element_by_id('sg-mm-9')
schedElem.click()
stuSchedElem = browser.find_element_by_xpath('//*[@id="mega-menu"]/div/div[1]/div/ul/li[2]/label')
stuSchedElem.click()
histElem = browser.find_element_by_xpath('//*[@id="mega-menu"]/div/div[2]/div/div/div[27]/div[1]/p[3]/a')
histElem.click()

#change number of students listed on screen
listBox = browser.find_element_by_xpath('//*[@id="search-results-grid_toppager_center"]/table/tbody/tr/td[8]/select')
listBox.click()
box1000 = browser.find_element_by_xpath('//*[@id="search-results-grid_toppager_center"]/table/tbody/tr/td[8]/select/option[7]')
box1000.click()
time.sleep(2)
#list definitions for later use
pelist = ["Dance", "Physical Education", "Girls Athletics", "Boys Athletics", "Pre Athletics", "Tennis", "PE"]
elemList = ["scheduleHistoryCard2017", "scheduleHistoryCard2018", "scheduleHistoryCard2019"]
present_list = ['2017', '2018', '2019']
nameList = []
eighthGraders = []
#using beautiful soup to parse the html in order to access the student's names from the site
searchElem = browser.find_element_by_class_name('sg-search-results-container')
someSoup = BeautifulSoup(searchElem.get_attribute('innerHTML'), features='html.parser')
nameRows = someSoup.findAll("tr", {"class": "ui-widget-content jqgrow ui-row-ltr"})
aTags = someSoup.findAll('a')

counter = 0
#the overall loop to get the PE classes that were taken

for names in aTags:
    str_name = str(names)
    #this if statement pulls the student's name from the beautiful soup string then ensures the name is on screen to be clicked
    if "/eSchoolPLUS/Student/Scheduling/History?StudentId=" not in str_name:
        continue
    pos = str_name.find('>')
    cut1 = str_name[pos+1:]
    pos2 = cut1.find('<')
    cut2 = cut1[:pos2].strip()
    kidNames = browser.find_element_by_partial_link_text(cut2)
    actions = ActionChains(browser)
    actions.move_to_element(kidNames).perform()
    browser.execute_script("window.scrollBy(0,100);")
    kidNames.click()
    kid = {"Name": cut2, "2017": [], "2018": [], "2019": []}
    #this loop searches through the years and grabs the PE classes that were taken
    for i in range(len(elemList)):
        try:
            checkElem = browser.find_element_by_id(elemList[i])
            soup = BeautifulSoup(checkElem.get_attribute('innerHTML'), features="html.parser")
            for row in soup.findAll("div", {"class": "row sg-data-row"}):
                henry = BeautifulSoup(str(row), features="html.parser")
                if len(henry.findAll("div", {"class" : "sg-body-cell-content sg-is-dropped-course"})) > 0:
                    continue
                for pe in pelist:
                    if pe in str(row) and pe not in kid[present_list[i]]:
                        kid[present_list[i]].append(pe)
            if len(kid[present_list[i]]) == 0:
                kid[present_list[i]].append('n/a')

        except NoSuchElementException:
            kid[present_list[i]].append('n/a')
    #this is appending all information found to the class_dict dictionary, going back to the main page, and maximizing the amount of students on screen
    eighthGraders.append(kid)
    browser.back()
    time.sleep(.2)
    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    time.sleep(.5)
    listBox = browser.find_element_by_xpath('//*[@id="search-results-grid_toppager_center"]/table/tbody/tr/td[8]/select')
    listBox.click()
    box1000 = browser.find_element_by_xpath('//*[@id="search-results-grid_toppager_center"]/table/tbody/tr/td[8]/select/option[7]')
    box1000.click()
    time.sleep(4)
df = pd.DataFrame(eighthGraders)
df = df[['Name', '2017', '2018', '2019']]
df.to_csv('C:\Excel Practice\pandas7.csv')
