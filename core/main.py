from fastapi import FastAPI,Depends
from contextlib import asynccontextmanager
from tasks.routes import router as tasks_routes
from users.routes import router as users_routes
from users.models import UserModel


tags_metadata = [
    {
        "name":"tasks",
        "description":"API for managing tasks with FastAPI",
        "externalDocs":{
            "description":"my github",
            "url":"https://github.com/shahinabbasidev"
        }
    }
]

@asynccontextmanager
async def lifespan(app=FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")

app = FastAPI(    
    title="Todo application",
    description="this is a section of description",
    version="0.0.1",
    contact={
        "name": "Shahin Abbasi",
        "url": "https://github.com/shahinabbasidev",
        "email": "shahin.abbasi.dev@gamil.com",
    },
    license_info={
        "name": "MIT",
    },lifespan=lifespan,openapi_tags=tags_metadata)
app.include_router(tasks_routes)
app.include_router(users_routes)

from auth.token_auth import get_authenticated_user




@app.get("/public")
async def public_authenticate():

    return {"message":"this is public route"}

@app.get("/private")
async def private_authenticate(user :get_authenticated_user= Depends(get_authenticated_user)):

    return {"message":"this is private route"}