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

    intent = body["queryResult"]
    return {
        "fulfillmentText": f"Intent: {intent}"
    }




if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)