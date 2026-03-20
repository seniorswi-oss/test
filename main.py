import fastapi
import uvicorn

API_BASE = "/api/v1"

app = fastapi.FastAPI()
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post(API_BASE + "/")
def create_order(item: str = fastapi.Form(...), qty: int = fastapi.Form(...)):
    with open("orders.txt", "a") as f:
        f.write(f"{item}: {qty}\n")
    return {"Item": item, "Quantity": qty}




if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)