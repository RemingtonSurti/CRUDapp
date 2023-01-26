from flask import Flask, request, jsonify, make_response, render_template, abort
from flask_cors import CORS
from datetime import datetime
from bson import ObjectId
from functools import wraps
import jwt
from BackEND.dboperations import users, employees, get_skill, check_user,get_skill_list, get_description_list, get_description, checkToAdd_emp, checkToUpdate_emp
from BackEND.jwt_handler import sign_JWT
from werkzeug.security import generate_password_hash, check_password_hash
from decouple import config


JWT_SECRET = config("Secret_KEY")
JWT_ALGO = config("algorithm")

app = Flask(__name__)
CORS(app)



@app.errorhandler(401)
def not_authorised(e):
    return jsonify({"err" :"Expired Token"})


#HOME 
@app.route('/')
def home():
    return render_template('login.html')



#JWT TOKEN VALIDITY CHECK DECORATOR
def check_token(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token= None
        if 'access_token' in request.headers: 
            token = request.headers['access_token']
        #token = request.args.get("access_token")
        if not token:
            return jsonify({
                    "err" : "Token is missing!! Log in Again.."
                }), 401
        try:
            data = jwt.decode(token, key = JWT_SECRET, algorithms = [JWT_ALGO,])
            if datetime.fromtimestamp(data['expiry']) <= datetime.utcnow():
                return make_response({"err" :"Timeout! Log in Again.."}, 401, {'WWW-Authenticate' : 'Basic realm = "Authentication Failed"'})
            current_user = check_user(data['userID'])       
        except Exception as e:
            return jsonify({
                    "err" : "Token is Invalid!! Log in Again.."
                }), 401
        return func(current_user,*args, **kwargs)
    return decorated


#LOGIN AND AUTHENTICATE
@app.route('/authenticate', methods=['POST']) 
def login_user():
    try:
        data = request.get_json()
        l = users.find_one({"Username" : data['username']})
        if l:
            if check_password_hash(l['Password'], data['password']):
                token = sign_JWT(data['username'])
                return jsonify({"access_token" : token['access_token'], "msg" : f"Welcome {data['username']}"})#, make_response("Verified!",200).set_cookie("abc",token['access_token'], max_age=timedelta(minutes=2)) #, App() #render_template('frontend/src/App.js')
            else:
                return make_response({"err" :"Verification Failed! Try Again"}, 401, {'WWW-Authenticate' : 'Basic realm = "Authentication Failed"'})
        else:
            return make_response({"err" :"Verification Failed! Try Again"}, 401, {'WWW-Authenticate' : 'Basic realm = "Authentication Failed"'})
    except Exception as e:
        return jsonify({"err" :"Unable to verify!"})#, make_response('ERROR!', 401, {'WWW-Authenticate' : 'Basic realm = "Authentication Failed"'})




#SHOW ALL EMPLOYEES
@app.route("/Employees", methods=['GET'])
@check_token
def show_employees(current_user):
    if not current_user:
        return jsonify({"err" :"Unable to verify!"}), 401
    emp_list = []
    skills_obj = []
    desc_obj = []
    sl = get_skill_list()
    dl = get_description_list()
    # for i in sl:
    #     skills_obj.append({"value" : i, "label": i})
    # for i in dl:
    #     desc_obj.append({"value" : i, "label": i})
    
    for doc in employees.find():
        temp = {
            "_id" : str(ObjectId(doc["_id"])),
            "First_Name" : doc['First_Name'],
            "Last_Name" : doc['Last_Name'],
            "DOB" : str(doc['DOB'].date()),
            "Email" : doc['Email'],
            "Skill" : get_skill(doc['Skill_Level']),
            "Level" : get_description(doc['Skill_Level']),
            "Active" : str(doc['Active']),
            "Age": doc['Age']
            }
        emp_list.append(temp)
    return jsonify({"employees": emp_list, "skills": sl, "levels" : dl})




 
#ADD EMPLOYEE
@app.route("/Employees", methods = ['POST'])
@check_token
def add_employee(current_user):#current_user):
    if not current_user:
        return make_response({"err" :"Unable to verify!"}, 401, {'WWW-Authenticate' : 'Basic realm = "Authentication Failed"'})
    emp = request.get_json()
    result = checkToAdd_emp(emp)
    return jsonify(result)




# UPDATE EMPLOYEE
@app.route("/Employees/<EmployeeId>", methods = ['PUT'])
@check_token
def update_employee(current_user, EmployeeId : str):
    if not current_user:
        return make_response({"err" :"Unable to verify!"}, 401, {'WWW-Authenticate' : 'Basic realm = "Authentication Failed"'})
    data = request.get_json()
    result = checkToUpdate_emp(data, EmployeeId)
    return jsonify(result)




#DELETE EMPLOYEE
@app.route("/Employees/<EmployeeId>", methods=['DELETE'])
@check_token
def delete_employee(current_user, EmployeeId : str):
    if not current_user:
        return make_response("Unable to verify!", 401, {'WWW-Authenticate' : 'Basic realm = "Authentication Failed"'})
    get_emp = employees.find_one({"_id" : ObjectId(EmployeeId)})
    if not get_emp:
        return jsonify({"err" : "Employee not found"})
    del_emp = employees.delete_one({"_id" : get_emp['_id']})
    return jsonify({"msg" : "Employee has been removed"})



@app.route('/signup', methods=['POST'])
def signup_user():
    try:
        data = request.get_json()
        user = users.find()
        if data and user:
            for doc in user:
                if doc['Username'] == data['username']:
                    if check_password_hash(doc["Password"],data["password"]):
                        return make_response({"err" : "User already exists"}, 401, {'WWW-Authenticate' : 'Basic realm = "Authentication Failed"'})    
            hashed_pwd = generate_password_hash( data['password'], method='sha256')
            users.insert_one({
                "Username" : data['username'],
                "Password" : hashed_pwd
                })
            token = sign_JWT(data['username'])
            return jsonify({"access_token" : token['access_token'], "msg" : f"Welcome {data['username']}"})
        else:
            return jsonify({'err': 'Internal Server Error!!'})
    except Exception as e:
        return jsonify(e)



@app.route("/Employee/<EmployeeId>", methods=['GET'])
@check_token
def show_employee(current_user, EmployeeId : str):
    if not current_user:
        return make_response("Unable to verify!", 401, {'WWW-Authenticate' : 'Basic realm = "Authentication Failed"'})
    for doc in employees.find():
        if doc['_id'] == ObjectId(EmployeeId):
            temp = {
                "_id" : str(ObjectId(doc["_id"])),
                "firstname" : doc['First_Name'],
                "lastname" : doc['Last_Name'],
                "email" : doc['Email'],
                "skill_name" : get_skill(doc['Skill_Level']),
                "skill_description" : get_description(doc['Skill_Level']),
                "Active" : doc['Active'],
                "Age": doc['Age']
                }
    return jsonify(temp)

        

if __name__ == '__main__':
    app.run(debug=True)
