import fastapi
import uvicorn

API_BASE = ""

app = fastapi.FastAPI()
@app.get("/")
def read_root():
    print("Received a GET request at /")
    return {"message": "Hello, World!"}, 200

@app.post("/webhook")
async def webhook(request: fastapi.Request):
    body = await request.json()

    intent = body["queryResult"]["intent"]["displayName"]
    params = body["queryResult"]["parameters"]

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
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)