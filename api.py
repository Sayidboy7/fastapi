from fastapi import FastAPI, Path, Query, HTTPException
import uvicorn
from pydantic import BaseModel

class Item(BaseModel):
	name : str
	age : int
	status : str = None


app = FastAPI()

inventory = {
	1 : {'name' : 'josh', 'age': 21, 'status' : 'active'},
	2 : {'name' : 'john', 'age': 19, 'status' : 'deactive'}
}


@app.get('/api/items')
def get_items():
	return {'items' : inventory}

@app.get('/api/get-item/{item_id}')
def get_item(item_id: int = Path(..., description='item id need to view the item')):
	if item_id not in inventory:
		raise HTTPException(status_code=404, detail='Item Not Found!')

	return inventory[item_id]

@app.post('/api/add-item')
def create_item(item : Item, item_id : int = None):
	if not item_id:
		item_id = len(inventory) + 1
	if item_id in inventory:
		raise HTTPException(status_code=400, detail='Item already exsists!')
	
	inventory[item_id] = item
	return inventory[item_id]


@app.put('/api/item/{item_id}')
def update_item(item_id: int, item : Item):
	if item_id not in inventory:
		raise HTTPException(status_code=404, detail='Item Not Found!')

	inventory[item_id] = item
	return inventory[item_id]


@app.delete('/api/item/delete/{item_id}')
def delete_item(item_id : int):
	if item_id not in inventory:
		raise HTTPException(status_code=404, detail='Item Not Found!')

	del inventory[item_id]
	return 200, {'success' : 'Item deleted!'}



if __name__ == '__main__':
	uvicorn.run(app)