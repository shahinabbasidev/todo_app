from sqlalchemy import Column,String,Integer,DateTime,func,Boolean,Text,ForeignKey
from core.database import Base
from sqlalchemy.orm import relationship

class TaskModel(Base):
    __tablename__= "tasks"

    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    title = Column(String(200),nullable=True)
    description = Column(Text(500),nullable=False)
    is_complete = Column(Boolean,default=True)
    create_date = Column(DateTime,server_default=func.now())
    update_date = Column(DateTime,server_default=func.now(),server_onupdate=func.now())

    user = relationship("UserModel",back_populates="task")