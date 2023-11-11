from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chromedriver import driver
from config import LINKS,NAMES
from json_functions import updateJSONOnce




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
dbList = []
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
                dbList.append(newDict)
updateJSONOnce(dbList)

                 
