import fastapi
import uvicorn

API_BASE = ""

app = fastapi.FastAPI()
@app.get("/")
def read_root():
    print("Received a GET request at /")
    return {"message": "Hello, World!"}

@app.post(API_BASE + "/")
async def create_order(request: fastapi.Request):
    print(f"Received a POST request at {API_BASE}/")
    body = await request.json()
    intent = body["queryResult"]
    print(intent)
    return {"fulfillmentText": "This is a response from the webhook!"}




if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)