from fastapi import FastAPI
import json
import uvicorn
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

def readJsonData(filePath):
  with open(filePath, 'r') as file:
    return json.load(file)

def writeJsonData(filePath, data):
  with open(filePath, 'w') as file:
    json.dump(data, file, indent=2, sort_keys=True, default=str)

# Pydantic model for request body
class Item(BaseModel):
  name: str
  symbol: str
  price: int
  marketcap: int
  created_at: datetime = ''
  updated_at: datetime = ''


    # get all items
@app.get("/items")
async def getAllItem():
  data = readJsonData('import.json')
  return data


# get a item by id
@app.get("/item/{id}")
async def getItemByID(id: int):
  data = readJsonData('import.json')
  findItem = {}
  for item in data:
    if id == item["id"]:
      findItem = item

  if len(findItem) == 0:
    return "Item not found!"
  return findItem


# create a item
@app.post("/item")
async def createItem(item: Item):
  data = Item(
    name = item.name, 
    symbol = item.symbol, 
    price = item.price, 
    marketcap = item.marketcap, 
    created_at = datetime.now(),
    updated_at = datetime.now()
  )
  writeJsonData('export.json', json.loads(data.model_dump_json()))
  return data


# update a item
@app.put("/item/{id}")
async def updateItem(item: Item, id: int):
  data = readJsonData('import.json')
  selectedData = {}
  newArr = []
  for el in data:
    if id == el["id"]:
      el = {
        **el,
        "name": item.name, 
        "symbol": item.symbol, 
        "price": item.price, 
        "marketcap": item.marketcap, 
        "updated_at": datetime.now(),
      }
      selectedData = el
    newArr.append(el)
  writeJsonData('import.json', newArr)

  if len(selectedData) == 0:
    return "Item not found!"
  return selectedData


# delete a item
@app.delete("/item/{id}")
async def deleteItem(id: int):
  data = readJsonData('import.json')
  selectedData = {}
  for item in data:
    if id == item["id"]:
      selectedData = item
      data.pop(data.index(item))
  writeJsonData('import.json', data)
  if len(selectedData) == 0:
    return "Item not found!"
  return data

if __name__ == '__main__':
  uvicorn.run('main:app', reload=True)