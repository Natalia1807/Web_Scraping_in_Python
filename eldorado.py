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

driver.get('https://www.eldorado.ru/')

assert 'Эльдорадо' in driver.title


pages = 0

time.sleep(5)

products_all = driver.find_element_by_xpath("//div[@class='sc-1eh2cxq-2 gRvPfA']")

while True:
        button = products_all.find_element_by_xpath(
            "//button[@class='sc-160x70i-1 sc-160x70i-3 iJLkZv slick-arrow slick-next']")
        pages += 1
        button.click()
        if button.get_attribute('class') == "sc-160x70i-1 sc-160x70i-3 iJLkZv slick-arrow slick-next slick-disabled":
            break


products = products_all.find_elements_by_xpath("//div[@class='zqgg6c-0 cAmgDX']")
more_interesting = []
for product in products:
        product_list = {}
        product_name = product.find_element_by_class_name('dZiceH').text
        # sale_price = product.find_element_by_class_name('fwyUvV').text
        price = product.find_element_by_class_name('kkJCtt').text
        # discount = product.find_element_by_class_name('jLVUOf').text
        link_1 = product.find_element_by_tag_name('a')
        link = link_1.get_attribute('href')
        product_list['link'] = link
        product_list['name'] = product_name
        product_list['price'] = price
        more_interesting.append(product_list)

print(more_interesting)


client = MongoClient('localhost', 27017)
db = client['eldorado_new']

db.eldorado_new.insert_many(more_interesting)
db.eldorado_new.delete_many({'name': None})
db.eldorado_new.update_many({'link': more_interesting['link']},
                                              {'$set': more_interesting},
                                              upsert=True
                                              )  ## не работает


driver.quit()

##Несолько дней промучилась с сайтом Эльдорадо. Сначала хотела собрать все данные с распродажи. Так и не поняла, почему не дохожу до этого
# блока, хотя xpath показвал,что это единственный элемент на странице. В итоге взяла тот, на которм программа останавлявалсь. Метод сбора данных
# был абсолютно аналогичный. В итоге даже в этом блоке собирались какие-то пустые значения и одно значение из другого блока. Я уже готова была
# душу дьяволу продать, но в итоге так и не получилось сделать корректно.

