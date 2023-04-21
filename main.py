import uvicorn
from fastapi import FastAPI
from routes.address_api import address_router

app = FastAPI()  # fastapi instance created
app.include_router(address_router, prefix="/address")

if __name__ == "__main__":
    uvicorn.run(app)  # to run app
