from pydantic import BaseModel,Field,field_validator


class UserLoginSchema(BaseModel):
    username : str = Field(...,max_length=250,description="username for user login")
    password : str = Field(...,description="password for login users")
    

    
class UserRegisterSchema(BaseModel):
    username : str = Field(...,max_length=250,description="username for user login")
    password : str = Field(...,description="password for register users")
    password_confirm : str = Field(...,description="confirm the password")

    @field_validator("password_confirm")
    def check_password_match(cls,password_confirm,validation):
        if not password_confirm == validation.data.get("password"):
            raise ValueError("password dosent match")
        return password_confirm
