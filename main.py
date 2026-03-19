import fastapi
import uvicorn

app = fastapi.FastAPI()
@app.post("/")
def read_root(item: str = fastapi.Form(...), qty: int = fastapi.Form(...)):
    return {"Item": item, "Quantity": qty}




if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)