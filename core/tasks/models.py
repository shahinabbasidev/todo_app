from sqlalchemy import Column,String,Integer,DateTime,func,Boolean,Text
from core.database import Base


class TaskModel(Base):
    __tabelname__= "tasks"

    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String(200),nullable=True)
    description = Column(Text(500),nullable=False)
    is_complete = Column(Boolean,default=True)
    create_date = Column(DateTime,server_default=func.now())
    update_date = Column(DateTime,server_default=func.now(),server_onupdate=func.now())