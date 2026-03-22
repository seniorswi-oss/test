import fastapi
import uvicorn
from database import database
import utils
import pandas as pd

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

    # order = database.fetch_items(4)
 

    # # order = utils.fetch_all_orders()

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
        if not order:
            utils.place_order(status = params['status'], session_id = params['session_id'])
        result = utils.fetch_all_items()
        result = pd.DataFrame(result)
        result = result.to_string(index=False)

    elif action == 'add-item':
        order = utils.get_order_by_session(session_id=session_id)
        order_id = order['order_id']
        utils.add_item_to_order(order_id=order_id, items=params['items'], qtys=params['qty'])
        result = "Items added successfully"

    elif action == 'remove-item':
        order = utils.get_order_by_session(session_id=session_id)
        order_id = order['order_id']
        qty = params['qty'] if params['qty'] else []
        utils.remove_item_from_order(order_id=order_id, items=params['items'], qtys=qty)
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