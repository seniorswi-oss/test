import fastapi
import uvicorn
from database import database
import utils

database.connect_db()

API_BASE = ""

app = fastapi.FastAPI()
@app.get("/")
def read_root():
    print("Received a GET request at /")
    return {"message": "Hello, World!"}, 200

@app.post("/db_create")
def db_create():
    print("Received a POST request at /db_create")
    database.init_db()
    return {"message": "Generated Database"}, 200

@app.post("/webhook")
async def webhook(request: fastapi.Request):

 

    # order = utils.fetch_all_orders()

    # print(order)
    # return {"message": "Webhook received"}, 200

    body = await request.json()

    print(body)

    # intent = body["queryResult"]["intent"]["displayName"]
    params = body["queryResult"]["parameters"]
    action = body["queryResult"]["action"]
    session_id = body["session"].split("/")[-1]
    params['session_id'] = session_id

    if action == 'place-order':
        params['status'] = 'pending'
        order = utils.get_order_by_session(session_id=session_id)
        print(order)
        if order:
            result = "You already have an active order. Please complete it before placing a new one."
        else:
            result = utils.place_order(status = params['status'], session_id = params['session_id'])
    elif action == 'add-item':
        order = utils.get_order_by_session(session_id=session_id)
        order_id = order['order_id']
        items = utils.fetch_all_items()
        for item in items:
            for i in params['items']:
                if item['name'] == i:
                    item_id = item['item_id']
                    utils.insert_order_item(order_id=order_id, item_id=item_id, qty=item['qty'], total=item['qty'] * item['total'])
        result = "Items added successfully"
    elif action == 'remove-item':
        order = utils.get_order_by_session(session_id=session_id)
        order_id = order['order_id']
        items = utils.fetch_all_items()
        for item in params['items']:
            item_id = items[item]['item_id']
            if item['qty']:
                utils.update_order_item(order_id=order_id, item_id=item_id, qty=item['qty'], total=item['qty'] * item['total'])
            else:
                utils.remove_order_item(order_id=order_id, item_id=item_id)
        result = "Items removed successfully"
    elif action == 'order-complete':
        params['status'] = 'completed'
        order = utils.get_order_by_session(session_id=session_id)
        params['order_id'] = order['order_id']
        utils.order_complete(order_id=params['order_id'], status=params['status'])
        result = "Order completed successfully"

    return {
        "fulfillmentMessages": [
            {
            "text": {
                "text": [
                    result
                ]
            }
            }
        ]
    }




if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)