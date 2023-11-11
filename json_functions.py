import json

#updates supplier dict
def Merge(dict1, dict2):
    return(dict2.update(dict1))

#convert JSON to a list of dicts
def getJSON():
    #read JSON file
    with open('assets.json') as file:
        items = json.load(file)
    #gather all SN into a dict
        return items

#dumps json
def updateJSON(items,x):
    allDb = getJSON()
    #current supplier dict
    currentDb = allDb[x]
    #update dict
    Merge(items,currentDb)
    json_object = json.dumps(allDb, indent=4)
    with open('assets.json', "w") as fileout:
         fileout.write(json_object)

#json function for feedr function
def updateJSONOnce(allDb):
    json_object = json.dumps(allDb,indent=4)
    with open('assets.json', "w") as fileout:
         fileout.write(json_object)