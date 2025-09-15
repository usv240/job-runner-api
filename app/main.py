# from fastapi import FastAPI
# from app.routes import router

# app = FastAPI(title="Job Runner API")

# app.include_router(router)
from fastapi import FastAPI
import uvicorn
from app.routes import router

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)