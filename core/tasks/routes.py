from fastapi import APIRouter,Path,Depends,HTTPException,Query,Body
from fastapi.responses import JSONResponse
from tasks.models import TaskModel
from users.models import UserModel
from tasks.schemas import TaskResponseSchema,TaskCreateSchema,TaskUpdateSchema
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List
from auth.jwt_aut import get_authenticated_user

router = APIRouter(tags=["tasks"],prefix="/todo")

@router.get("/tasks",response_model=List[TaskResponseSchema])
async def retrieve_tasks_list(
    completed: bool = Query(None,description="Filter tasks based on being completed or no"),
    limit: int = Query(10, gt=0, le=50,description="Limiting the number of items to retrieve"),
    offset: int = Query(0, gt=-1,description="Use for paginating based on passed items"),
    user: UserModel = Depends(get_authenticated_user),
    db:Session = Depends(get_db)):

    query = db.query(TaskModel).filter_by(user_id = user.id)
    if completed is not None:
        query = query.filter_by(is_complete = completed)
    
    return query.limit(limit).offset(offset).all()

@router.get("/tasks/{task_id}",response_model=TaskResponseSchema)
async def retrieve_tasks_detail(task_id: int = Path(...,gt=0),db:Session = Depends(get_db),user: UserModel = Depends(get_authenticated_user)):

    task_obj = db.query(TaskModel).filter_by(user_id = user.id,id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404,detail="task not found")
    return task_obj


@router.post("/tasks")
async def post_tasks(request:TaskCreateSchema,db:Session = Depends(get_db),user: UserModel = Depends(get_authenticated_user)):
    data = request.model_dump()
    data.update({"user_id":user.id})
    task_obj = TaskModel(**data)
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    return task_obj


@router.put("/tasks/{task_id}",response_model=TaskResponseSchema)
async def put_tasks(request:TaskUpdateSchema = Body(...),task_id: int = Path(...,gt=0),db:Session = Depends(get_db),user: UserModel = Depends(get_authenticated_user)):
    task_obj = db.query(TaskModel).filter_by(user_id = user.id,id = task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for field, value in request.model_dump(exclude_unset=True).items():
        setattr(task_obj,field,value)
    db.commit()
    db.refresh(task_obj)

    return task_obj

@router.delete("/tasks/{task_id}",status_code=204)
async def delete_tasks(task_id: int = Path(...,gt=0),db:Session = Depends(get_db),user: UserModel = Depends(get_authenticated_user)):
    task_obj = db.query(TaskModel).filter_by(user_id = user.id,id = task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task_obj)
    db.commit()
    return task_obj
