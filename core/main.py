from fastapi import FastAPI
from contextlib import asynccontextmanager
from tasks.routes import router as tasks_routes

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