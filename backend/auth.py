from typing import Union

from fastapi import FastAPI,Depends
import uvicorn
import requests

app = FastAPI()


@app.get("/")
def read_root():
    temp=[]
    data=requests.get('https://dummyjson.com/products')
    data=data.json()
    return data


def fetch_data():
    """Fetch data from API and return it as JSON."""
    response = requests.get("https://dummyjson.com/products")
    return response.json()

@app.get("/")
def read_root():
    temp=[]
    data=requests.get('https://dummyjson.com/products')
    data=data.json()
    return data


@app.get("/{item_price}")
async def read_item(item_price: int,data:dict =Depends(fetch_data)):
    
    filtered_data=list(filter(lambda x: x['price'] >=item_price, data['products']))
    return filtered_data
    
    # if q:
    #     return {"item_id": item_id, "q": q}
    # return {"item_id": item_id}



@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')