from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from pymongo import MongoClient
import json
import pprint
chrome_options = Options()
chrome_options.add_argument('start-maximized')


driver = webdriver.Chrome(options=chrome_options)

driver.get('https://mail.ru')
assert 'Mail.ru'  in driver.title  #Проверяем на той ли мы страницы

# html = driver.page_source

elem = driver.find_element_by_id('mailbox:login')
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.RETURN)

time.sleep(3)

elem = driver.find_element_by_id('mailbox:password')
elem.send_keys('NewPassword172')
elem.send_keys(Keys.RETURN)

time.sleep(5)


first_letter_container = driver.find_element_by_xpath("//div[@class='llc__container']")
# # first_letter = driver.find_element_by_tag_name('dataset-letters')
first_letter_container.click()
# time.sleep(3)
# back = driver.find_element_by_class_name('portal-menu-element_back')
# back.click()
# time.sleep(3)
# next_letter = driver.find_element_by_class_name('dataset-letters')  #g-silent
# next_letter.click()


mails_list = []

while True:
    mail_info = {}
    time.sleep(3)
    sender = driver.find_element_by_xpath("//div[@class='letter__author']/span[@class='letter-contact']").text
    date = driver.find_element_by_class_name('letter__date').text
    title = driver.find_element_by_class_name('thread__subject_pony-mode').text
    text = driver.find_element_by_class_name('letter-body').text

    mail_info['title'] = title
    mail_info['date'] = date
    mail_info['sender'] = sender
    mail_info['text'] = text
    mails_list.append(mail_info)

    next_letter = driver.find_element_by_class_name('portal-menu-element_next')

    next_letter.click()
    if next_letter .get_attribute('class') == "button2 button2_has - ico button2_arrow - down button2_pure button2_short button2_compact button2_ico - text - topbutton2_hover - support button2_disabled js - shortcut":
        break

client = MongoClient('localhost', 27017)
db = client['letters_parser']

db.letters_parser.insert_many(mails_list)
db.letters_parser.update_many({'link': mails_list['link']},
                                              {'$set': mails_list},
                                              upsert=True
                                              )  ## не работает


driver.quit()