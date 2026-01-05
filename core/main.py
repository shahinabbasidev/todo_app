from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from users.models import UserModel
from auth.jwt_aut import get_authenticated_user
from tasks.routes import router as tasks_routes
from users.routes import router as users_routes


tags_metadata = [
    {
        "name": "tasks",
        "description": "API for managing tasks with FastAPI",
        "externalDocs": {
            "description": "My GitHub",
            "url": "https://github.com/shahinabbasidev"
        }
    }
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")


app = FastAPI(
    title="Todo application",
    description="This is a section of description",
    version="0.0.1",
    contact={
        "name": "Shahin Abbasi",
        "url": "https://github.com/shahinabbasidev",
        "email": "shahin.abbasi.dev@gmail.com",
    },
    license_info={"name": "MIT"},
    lifespan=lifespan,
    openapi_tags=tags_metadata
)

app.include_router(tasks_routes)
app.include_router(users_routes)


@app.get("/public")
async def public_authenticate():
    return {"message": "This is public route"}


@app.get("/private")
async def private_authenticate(user: UserModel = Depends(get_authenticated_user)):
    return {"message": "This is private route", "user": user.username}