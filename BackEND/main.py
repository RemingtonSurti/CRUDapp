from fastapi import FastAPI, Body, HTTPException, Depends, requests
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from bson import ObjectId
from model import userLoginSchema, getemployeeSchema, addemployeeSchema, skill_levelSchema
from jwt_handler import sign_JWT
from jwt_bearer import jwt_bearer
from dboperations import users, employees, skill_level, checkToAdd_emp, get_employee, get_skill
from datetime import datetime

app = FastAPI()

origins = ["http://127.0.0.1:8000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"])

@app.get("/")
def greet():
    return {"Hello" : "World"}

def check_user(data : userLoginSchema):
    try:
        l = users.find_one({ "$and" : [{"Username" : data['username']}, {"Password" : data['password']}]})
        if l:
            return True
        else:
            return False
    except Exception as e:
        print(e)




@app.post("/Authenticate")
def authenticate_user(user : userLoginSchema = Body(default=None)):
    try:
        if not check_user(user):
            raise HTTPException(status_code=404, detail="Invalid login details")
        else:
            return JSONResponse(sign_JWT(user['username']))     
    except Exception as e:
        return e





@app.get("/Employees")
def show_employees():
    pass



@app.post("/Employees")
def add_employee(emp : getemployeeSchema):
    result=jsonable_encoder(checkToAdd_emp(emp))
    return JSONResponse(content=result)


@app.put("/Employees/{EmployeeId}", dependencies=[Depends(jwt_bearer())])
def update_employee():
    pass





@app.delete("/Employees/{EmployeeId}", dependencies=[Depends(jwt_bearer())])
def delete_employee():
    pass

if(__name__)=='__main__':
    app.run(debug=True)