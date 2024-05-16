from fastapi import FastAPI
from frcm.routes import router

app = FastAPI()
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "FireGuard Cloud Service"}
