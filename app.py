from flask import Flask, request, jsonify, make_response, render_template, session
from datetime import datetime
from time import time
from bson import ObjectId
from functools import wraps
import jwt
from BackEND.dboperations import users, employees, get_skill, check_user, checkToAdd_user_pass
from BackEND.jwt_handler import sign_JWT
from werkzeug.security import generate_password_hash, check_password_hash
from decouple import config


JWT_SECRET = config("Secret_KEY")
JWT_ALGO = config("algorithm")

app = Flask(__name__)
app.config['SECRET_KEY'] =  config("Mongo_KEY")

def check_token(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token= None
        if 'access_token' in request.headers: 
            token = request.headers['access_token']
        #token = request.args.get("access_token")
        if not token:
            return jsonify({
                    "Alert" : "Token is missing!!"
                }), 401
        try:
            data = jwt.decode(token, key = JWT_SECRET, algorithms = [JWT_ALGO,])
            if datetime.fromtimestamp(data['expiry']) <= datetime.utcnow():
                return {"Alert" :"Expired Token"}
            current_user = check_user(data['userID'])       
        except Exception as e:
            return jsonify({
                    "Alert" : "Token is Invalid!!"
                }), 401
        return func(current_user,*args, **kwargs)
    return decorated


#HOME 
@app.route('/')
def home():
    return render_template('login.html')

#PUBLC ACCESS
@app.route('/public')
def greet():
    return jsonify('For Public!')

#PRIVATE ACCESS
@app.route('/auth')
@check_token
def auth():
    return jsonify({'msg' :  'JWT verified!'})

@app.route('/signup', methods=['POST'])
def signup_user():
    try:
        data = request.get_json()
        checkToAdd_user_pass(data)
        l = users.find_one({"Username" : data['Username']})
        if l:
            return jsonify({"msg" : "Username already exists"})
        else:
            hashed_pwd = generate_password_hash( data['Password'], method='sha256')
            users.insert_one({
                "Username" : data['Username'],
                "Password" : hashed_pwd
                })
        return jsonify({"msg" :"User added Successfully"})
    except Exception as e:
        print(e)
    #return make_response('Couldnt verify!', 401, {'WWW-Authenticate' : 'Basic realm = "Login Required"'})


#LOGIN AND AUTHENTICATE
@app.route('/authenticate', methods=['POST']) 
def login_user():
    l = users.find_one({"Username" : request.form['username']})
    if l:
        if check_password_hash(l['Password'], request.form['password']):
            token = sign_JWT(request.form['username'])
            return jsonify(token)
        else:
            make_response('Unable to verify', 401, {'WWW-Authenticate' : "Basic realm : 'Authentication Failed'"})
    else:
        return make_response('Unable to verify', 401, {'WWW-Authenticate' : "Basic realm : 'Authentication Failed'"})




#SHOW ALL EMPLOYEES
@app.route("/Employees", methods=['GET'])
@check_token
def show_employees(current_user):
    if not current_user:
        return jsonify({"msg":"No token" })
    emp_list = []
    for doc in employees.find():
        temp = {
                "First Name" : doc['First Name'],
                "Last Name" : doc['Last Name'],
                "DOB" : doc['DOB'],
                "Email" : doc['Email'],
                "Skill Level" : doc['Skill Level'],
                "Active" : doc['Active'],
                "Age": doc['Age']
                }
        emp_list.append(temp)
    return jsonify(emp_list)



 
#ADD EMPLOYEE
@app.route("/Employees", methods = ['POST'])
@check_token
def add_employee(current_user):
    if not current_user:
        return jsonify({"msg":"No token" })
    emp = request.get_json()
    l = employees.find_one({ "$or" : [{"First Name" : emp['firstname']}, {"Email" : emp['email']}]})
    if l:
        return jsonify({"msg":"Employee already exists"})
    add_emp = {
                "First Name" : emp['firstname'],
                "Last Name" : emp['lastname'],
                "DOB" : datetime(emp['yr'], emp['mon'], emp['day']),
                "Email" : emp['email'],
                "Skill Level" : [get_skill(emp['skill_name'], emp['skill_description'])],
                "Active" : emp['Active'],
                "Age": emp['Age']
                }
    doc = employees.insert_one(add_emp)
    return jsonify({"msg":"Employee added Successfully"})






# UPDATE EMPLOYEE
@app.route("/Employees/<EmployeeId>", methods = ['PUT'])
@check_token
def update_employee(current_user, EmployeeId : str):
    if not current_user:
        return jsonify({"msg":"No token" })
    data = request.get_json()
    if not data:
        return jsonify({"ERROR" : "data not found"})
    get_emp = employees.find_one({"_id" : ObjectId(EmployeeId)})
    if not get_emp:
        return jsonify({"ERROR" : "Employee not found"})
    new_details = {
        "First Name" : data['firstname'],
                "Last Name" : data['lastname'],
                "DOB" : datetime(data['yr'], data['mon'], data['day']),
                "Email" : data['email'],
                "Skill Level" : [get_skill(data['skill_name'], data['skill_description'])],
                "Active" : data['Active'],
                "Age": data['Age']
        }
    update_emp = employees.update_one({"_id" : ObjectId(EmployeeId)}, {"$set" : new_details})
    if update_emp:
        return jsonify({"Employee updated" : "Employee has been updated"})




#DELETE EMPLOYEE
@app.route("/Employees/<EmployeeId>", methods=['DELETE'])
@check_token
def delete_employee(current_user, EmployeeId : str):
    if not current_user:
        return jsonify({"msg":"No token" })
    get_emp = employees.find_one({"_id" : ObjectId(EmployeeId)})
    if not get_emp:
        return jsonify({"ERROR" : "Employee not found"})
    del_emp = employees.delete_one({"_id" : get_emp['_id']})
    return jsonify({"msg" : "Employee has been removed"})

        

if __name__ == '__main__':
    app.run(debug=True)
