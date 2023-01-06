from pydantic import BaseModel, BaseConfig, Field, EmailStr
from bson import ObjectId
from datetime import datetime


class userLoginSchema(BaseModel):
    username : str = Field(default=None)
    password : str = Field(default=None)

    def __getitem__(self, item):
        return getattr(self, item)
    
    class Config:
        login_schema = {
            "login_demo" : {
                "username" : "Remo",
                "password" : "Remo"
            }
        }
    

class addemployeeSchema(BaseModel):
    firstname : str = Field(default=None)
    lastname : str = Field(default=None)
    DOB : datetime = Field(default=None)
    email : EmailStr = Field(default=None)
    skill_level : list = Field(default=None)
    Active : bool = Field(default=None)
    Age : int = Field(default=None)

    def __getitem__(self, item):
        return getattr(self, item)

    class Config:
        t2_schema = {
            "employee_demo" : {
                "firstname" : "Remington",
                "lastname" : "Surti",
                "DOB" : "employee's date of birth",
                "email" : "employee@email.com",
                "skill_level" : ["list of skills"],
                "isActive" : True,
                "Age" : 24
            }
        }

class getemployeeSchema(BaseModel): 
    firstname : str = Field(default=None)
    lastname : str = Field(default=None)
    yr : int = Field(default=None)
    mon : int = Field(default=None)
    day : int = Field(default=None)
    email : EmailStr = Field(default=None)
    skill_name : str = Field(default=None)
    skill_description : str = Field(default=None)
    Active : bool = Field(default=None)
    Age : int = Field(default=None)
    

    class Config:
        t2_schema = {
            "getemployee_demo" : {
                "_id" : "unique id",
                "firstname" : "Remington",
                "lastname" : "Surti",
                "yr" : "employee's year of birth",
                "mon" : "employee's month of birth",
                "day" : "employee's date of birth",
                "email" : "employee@email.com",
                "skill_name" : "name of skill",
                "skill_description" : "description of skill level",
                "isActive" : True,
                "Age" : 24
            }
        }  

class skill_levelSchema(BaseModel):
    skillname : str = Field(default=None)
    skilldescription : str = Field(default=None)

    def __getitem__(self, item):
        return getattr(self, item)

    class Config:
        t3_schema = {
            "skilllevel_demo" : {
                "skillname" : "Python",
                "skilldescription" : "skill proficiency"
            }
        }