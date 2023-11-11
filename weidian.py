from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chromedriver import driver
from json_functions import getJSON,updateJSON
import requests
import time
from config import BOT_API_KEY,CHAT_ID,LINKS,NAMES


##&& compare new items to existing on DB
def compareDBKeys(newDict,supplierIndex):
     currentDB = getJSON()
     currentSupplierDb = currentDB[supplierIndex]
     CSkeys = currentSupplierDb.keys()
     newKeys = newDict.keys()     
     relevantKeys = set(newKeys) - set(CSkeys)
     return {y:newDict[y] for y in newDict if y in relevantKeys}

##&& sends a custom telegram message
def sendMessage(newItem):
    #telegram message compose
    MY_MESSAGE_TEXT = f'''
{newItem["supplier"]}

{newItem["name"]}

{newItem["price"]}

{newItem["date"]}

{newItem['image'] if newItem['image'] != None else 'image is null '}
'''
    r = requests.get(
        f'https://api.telegram.org/{BOT_API_KEY}/sendMessage?chat_id={CHAT_ID}&text={MY_MESSAGE_TEXT}')
    if r.status_code == 200:
        #add supplier name 
        print(f'new item! - {newItem["supplier"]}')
    else:
        print(r.text["error_code"])  # Do what you want with response
        #telegram server error code 429 = too many requests, please retry after X seconds
        if r.text["error_code"] == 429:
             waitFor = r.text["parameters"]["retry_after"]
             print(f"we overloaded the telegram bot, lets wait for {waitFor} before trying again.")
             time.sleep(waitFor)

##&& converts a module to an item in a dict
def genItemsDict(moduleList,supplierNameIndex):
    itemsDict = {}
    for y in moduleList:
        dateCell = y.find_element(By.CLASS_NAME, 'cell')
        dateText = dateCell.find_element(By.CLASS_NAME, 'base-ct.txt').text
        itemsList = y.find_element(By.CLASS_NAME, 'list')
        items = itemsList.find_elements(By.CLASS_NAME, 'item')
        for z in items:
            imageContainer = z.find_element(By.CLASS_NAME, 'base-ct.img-wrapper')
            imageElement = imageContainer.find_element(By.TAG_NAME, 'img')
            image = imageElement.get_attribute('data-src')      
            name = z.find_element(By.CSS_SELECTOR,'.base-ct.txt').text
            cells = z.find_elements(By.CLASS_NAME,'cell')
            for cell in cells:
                cellText = cell.text.split('\n')
                if '￥' in cellText:
                    yuanIndex = cellText.index('￥')
                    price = f'{cellText[yuanIndex+1]}￥'
            itemsDict[name] = {'date':dateText,'name':name,'image':image,'price':price, 'supplier':NAMES[supplierNameIndex]}
    return itemsDict

##**                    START                   **##
while 1:
    dbList = getJSON()
    for x in range(len(LINKS)):
        ##&&    get link
                driver.get(LINKS[x])

        ##&&    try finding the items list,
        ##&&    if failed then all scraping is reset
                try:
                    element = WebDriverWait(driver, 100).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'module')))
                except:
                    print("couldn't find elements. refreshhh")
                    driver.refresh()
                    break

        ##&&    capture list after assuring that it exists
                modules = driver.find_elements(By.CLASS_NAME, 'module')

        ##&&    generating dict according to HTML
                newDict = genItemsDict(modules,x)

        ##&&    compare new items to existing on DB
                newItemsDict = compareDBKeys(newDict,x)

        ##&&    send Telegram message for each new item
                for z in newItemsDict:
                    sendMessage(newItemsDict[z])

        ##&&    update JSON file with new items
                updateJSON(newItemsDict,x)
                 
