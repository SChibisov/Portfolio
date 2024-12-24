from fastapi import FastAPI
import uvicorn
from routes.routes import user_router, product_router, cart_router


app = FastAPI()


app.include_router(user_router, prefix="/users")

app.include_router(product_router, prefix="/products")

app.include_router(cart_router, prefix="/carts")

if __name__ == " main ":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
