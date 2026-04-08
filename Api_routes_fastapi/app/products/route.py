from fastapi import APIRouter

app = APIRouter()

@app.get("/products",tags=["products"])
async def get_products():
  return {"message":'this is the prodcuts endpoint'}

@app.get("/sell_products",tags=["sell_products"])
async def sell_products():
  return {"message":'this is the Sell  prodcuts endpoint'}
