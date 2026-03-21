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
    return {"message": "Generated Database"}, 200

@app.post("/webhook")
async def webhook(request: fastapi.Request):
    body = await request.json()

    print(body)

    intent = body["queryResult"]["intent"]["displayName"]
    params = body["queryResult"]["parameters"]
    action = body["queryResult"]["action"]

    action_lists = ['place-order', 'add-item', 'remove-item']

    if action in action_lists:
        action = action.replace('-', '_')
        func = getattr(utils, action)
        result = func(**params)
    elif action == 'order-complete':
        result = utils.order_complete()

    print(action)
    print(intent)
    print(params)
    return {
        "fulfillmentMessages": [
            {
            "text": {
                "text": [
                "Text response from webhook"
                ]
            }
            }
        ]
    }




if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)