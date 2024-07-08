from fastapi import FastAPI,  Query, Request
import uuid
from datetime import datetime
import json
import uvicorn
from unidecode import unidecode
import jsonlines

app = FastAPI()

def read_file(file_path):
  with jsonlines.open(file_path) as reader:
    file_data = []
    for obj in reader:
      # Process each JSON object (obj) as needed
      file_data.append(obj)
    return file_data

def paginate(items, page, limit):
    start_index = (page - 1) * limit
    end_index = start_index + limit
    return items[start_index:end_index]

def write_file(file_path, obj, write_method):
  with open(file_path, write_method) as file:
    json_line = json.dumps(obj)
    file.write(json_line + '\n')  

# name: str = '', price: str = ''
@app.get('/products')
async def getItems(page: int = Query(default = 1),
                   limit: int = Query(default = 1),
                   name: str = '', job: str = ''):
  file_data = read_file('data.jsonl')
  if name or job:
    filter_data = []
    for row in file_data:
      if name and job and (name in unidecode(row["name"].lower())) and (job in unidecode(row["job"].lower())):
        filter_data.append(row)
      elif name and (name in unidecode(row["name"].lower())):
        filter_data.append(row)
      elif job and (job in unidecode(row["job"].lower())):
        filter_data.append(row)
    return paginate(filter_data, page, limit)
  return paginate(file_data, page, limit)

@app.post('/product')
async def createProduct(
    name: str, 
    age: int, 
    job: str = ''):
  print("name:" + name)
  print("age:" + age)
  print("job:" + job)
  payload = {
    "id": str(uuid.uuid4()),
    "name": name,
    "age": age,
    "job": job,
    "created_at": str(datetime.now()),
    "updated_at": str(datetime.now()),
  }
  write_file('data.jsonl', payload, 'a')
  return payload

@app.delete('/product/{product_id}')
async def deleteProduct(product_id: str):
  file_data = read_file('data.jsonl')
  findProduct = [product for product in file_data if product["id"] == product_id]
      
  if findProduct:
    for product in file_data:
      if product["id"] != product_id:
        write_file('data.jsonl', product, 'a')
    return "Delete product success!"
  else:
    return "Product not found!"


if __name__ == '__main__':
  uvicorn.run()