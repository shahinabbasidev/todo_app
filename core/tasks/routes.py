from fastapi import APIRouter,Path,Depends,HTTPException,Query
from fastapi.responses import JSONResponse
from tasks.models import TaskModel
from tasks.schemas import TaskResponseSchema,TaskCreateSchema,TaskUpdateSchema
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List

router = APIRouter(tags=["tasks"],prefix="/todo")

@router.get("/tasks",response_model=List[TaskResponseSchema])
async def retrieve_tasks_list(db:Session = Depends(get_db)):

    result = db.query(TaskModel).all()
    return result

@router.get("/tasks/{task_id}",response_model=TaskResponseSchema)
async def retrieve_tasks_detail(task_id: int = Path(...,gt=0),db:Session = Depends(get_db)):

    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404,detail="task not found")
    return task_obj


@router.post("/tasks",response_model=TaskResponseSchema)
async def post_tasks(db:Session = Depends(get_db),request = TaskCreateSchema):
    task_obj = TaskModel(**request.model_dump())
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    return task_obj


@router.put("/tasks/{task_id}",response_model=TaskResponseSchema)
async def put_tasks(task_id: int = Path(...,gt=0),db:Session = Depends(get_db),request = TaskUpdateSchema):
    task_obj = db.query(TaskModel).filter_by(id = task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for field, value in request.model_dump(exclude_unset=True).items():
        setattr(task_obj,field,value)
    db.commit()
    db.refresh(task_obj)

    return task_obj

@router.delete("/tasks/{task_id}",status_code=204)
async def delete_tasks(task_id: int = Path(...,gt=0),db:Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id = task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task_obj)
    db.commit()