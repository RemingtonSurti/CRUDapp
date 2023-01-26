import pymongo
from bson import ObjectId
from datetime import datetime, date
from BackEND.model import userLoginSchema
from BackEND.jwt_handler import sign_JWT
from decouple import config
from werkzeug.security import check_password_hash, generate_password_hash
import pprint


connection_string = f"mongodb+srv://mongodb:{config('Mongo_PWD')}@trainingdb.c92yljh.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
client = pymongo.MongoClient(connection_string) 
db = client.EmployeeDB

users = db['Users']
employees = db['Employees']
skill_level = db['Skill Levels']

# CHECK EXISTING USERS
def check_user(data : str):
    try:
        l = users.find_one({"Username" : data})
        if l:
            return l
        return {"msg" : "Invalid user datails", "msgtype" : ""}, 401
    except Exception as e:
        print(e) 

# GET LIST OF SKILLS
def get_skill_list() -> list:
    sl = []
    temp = skill_level.find()
    for doc in temp:
        if doc:
            x = doc['Skill_Name']
            if x not in sl:
                sl.append(x)
    return sl

# GET LIST OF DESCRIPTIONS
def get_description_list() -> list:
    dl = []
    temp = skill_level.find()
    for doc in temp:
        if doc:
            x = doc['Skill_Description']
            if x not in dl:
                dl.append(x)
    return dl



# GET VALID SKILL OBJECT
def fetch_skill_object(skillname : str, skilldescription : str) -> object:
    try:
        if skillname and skilldescription:
            skill_id = skill_level.find_one({ "$and" : [{"Skill_Name" : skillname.strip()}, {"Skill_Description" : skilldescription}]})
            if skill_id:
                return {
                    "Skill_Level_ID" : str(skill_id['_id']),
                    "Skill_Name" : skillname,
                    "Skill_Description" : skilldescription
                    }
            else:
                return {
                "msg" : "Invalid skill"
                }
    except Exception as e:
        print(e)


# GET A PARTICULAR SKILL
def get_skill(skill : list):
    try:
        if skill:
            return (skill[0])['Skill_Name']
        else:
            return{"msg" : "Invalid skill"}
    except Exception as e:
        print(e)

# GET A PARTICULAR DESCRIPTION
def get_description(skill : list):
    try:
        if skill:
            return (skill[0])['Skill_Description']
        else:
            return{"msg" : "Invalid Level"}
    except Exception as e:
        print(e)

# SET AGE
def get_age(dob : datetime) -> int:
    try:
        if dob:
            today = date.today()
            dob = dob.date()
            age = (today.year - dob.year)-((today.month, today.day)<(dob.month, dob.day))
            return age
        else:
            return{"msg" : "Invalid date"}
    except Exception as e:
        print(e)

# GET AN EMPLOYEE DOCUMENT
def get_employee(employee_ID : ObjectId) -> object:
    try:
        employee_object = employees.find_one({"_id" : employee_ID})
        ep_firstname = str(employee_object['First_Name'])
        ep_lastname = str(employee_object['Last_Name'])
        return {
            "firstname" : ep_firstname,
            "lastname" : ep_lastname
        }
    except Exception as e:
        print(e)

# CHECKING USER DETAILS BEFORE ADDING
def checkToAdd_user_pass(data : userLoginSchema) -> object:
    try:
        user = users.find()
        if user:
            for doc in user:
                if doc['Username'] == data['username']:
                    if check_password_hash(doc["Password"],data["password"]):
                        return {"err" : "Username already exists"}    
            hashed_pwd = generate_password_hash( data['password'], method='sha256')
            users.insert_one({
                "Username" : data['username'],
                "Password" : hashed_pwd
                })
            token = sign_JWT(data['username'])
            return {"access_token" : token['access_token'], "msg" : f"Welcome {data['username']}"}
        else:
            return {'err' : 'Database Connection error'}
    except Exception as e:
        print(e)

# CHECKING EMPLOYEE DETAILS BEFORE ADDING
def checkToAdd_emp(emp) -> object:
    l = employees.find_one({ "$or" : [{"First_Name" : emp['firstname']}, {"Email" : emp['email']}]})
    if l:
        return {"err":"Employee already exists"}
    temp = ""
    dob = datetime.strptime(emp['DOB'], '%Y-%m-%d')
    if emp['Active'] == "true":
        temp = "true"
    add_emp = {
                "First_Name" : emp['firstname'],
                "Last_Name" : emp['lastname'],
                "DOB" : dob,
                "Email" : emp['email'],
                "Skill_Level" : [fetch_skill_object(emp['skill_name'], emp['skill_description'])],
                "Active" : bool(temp),
                "Age": get_age(dob)
                }
    doc = employees.insert_one(add_emp)
    return {"msg":"Employee added Successfully"}

# CHECKING EMPLOYEE DETAILS BEFORE UPDATING
def checkToUpdate_emp(data, id) -> object:
    temp=""
    dob = datetime.strptime(data['DOB'], '%Y-%m-%d')
    if not data:
        return {"err" : "Employee not found"}
    get_emp = employees.find_one({"_id" : ObjectId(id)})
    if not get_emp:
        return {"err" : "Employee not found"}
    if data['Active'] == "true":
        temp = "true" 
    new_details = {
                "First_Name" : data['firstname'],
                "Last_Name" : data['lastname'],
                "DOB" : dob,
                "Email" : data['email'],
                "Skill_Level" : [fetch_skill_object(data['skill_name'], data['skill_description'])],
                "Active" : bool(temp),
                "Age": get_age(dob)
                }
    update_emp = employees.update_one({"_id" : ObjectId(id)}, {"$set" : new_details})
    if update_emp:
        return {"msg" : "Employee has been updated"}
            

# CHECKING SKILL DETAILS BEFORE ADDING
def checkToAdd_skill(skillname : str, skilldescription : str) -> object:
    try:
        l = skill_level.find_one({ "$and" : [{"Skill_Name" : skillname}, {"Skill_Description" : skilldescription}]})
        if l:
            return {"msg" : "Skill already exists"}
        else:
            skill_level.insert_one({
                "Skill_Name" : skillname,
                "Skill_Description" : skilldescription
                })
            return {"msg" : "New Skill added Successfully"}
    except Exception as e:
        print(e)





# try:
#     # log = []
#     # s = ["Python", "HTML", "C#", ".NET", "JavaScript", "React", "Angular", "MongoDB", "MySQL", "JAVA", "C++", "Scala", "SQL Server", "Business"]
#     # d = ["Beginner", "Intermediate", "Advanced", "Expert"]
#     # for i in s:
#     #     for j in d:
#     #         t=checkToAdd_skill(i, j)
#     a = get_skill_list()
#     b = get_description_list()
#     print(a)
#     print(b)
# except Exception as e:
#    print(e)    
     


# try:
    #encrypter = Fernet(encrypt_key)
    #test = get_skill("Python", "Advanced")
    #test1 = get_employee(ObjectId('63a606bb85815fba95cc588c'))
    # x = users.find_one({"Username" : "Cristiano"})
    # print(x)
    # print(check_password_hash(x['Password'], "Ronaldo"))
    # test2 = checkToAdd_user_pass({
    #     "username" : "Remo",
    #     "password" : generate_password_hash("Remo", method='sha256')
    #     })
    # data = users.find()
    # #l = users.find_one({ "$and" : [{"Username" : data['Username']}, {"Password" : data['Password']}]})
    # for doc in data:
    #     if doc['Username'] == "abc":
    #         print(doc['Password'])
    #         pwd = doc['Password']
    #         DD = encrypter.decrypt(pwd)
    #         DD.decode()
    #         print(DD)
    #         if DD == "Remo":
    #             print("User verified")
    #         print("Invalid details")

    # temp = doc['Password'].decode()
    # ED = encrypter. encrypt(temp)
    # print(ED)
    # DD = encrypter.decrypt(ED)
    # DT = DD.decode()
    # print(DT)

            # if  x == "Remo":
            #     print(x)
            # else:
            #     print("NA")

    #t = "abc"

    #t = users.insert_one(admin_dict)
    # test3 = checkToAdd_emp({
    #     "firstname": "Pankti",
    #     "lastname": "Gohil",
    #     "yr": 1999,
    #     "mon": 9,
    #     "day": 11,
    #     "email": "Pankti@Gohil.com",
    #     "skill_name": "Python",
    #     "skill_description": "Expert",
    #     "Active": True,
    #     "Age": 22
    #     })
    # test4 = checkToAdd_skill({
    # "Employee ID" : ObjectId(),
    # "Skill_Name" : "Python",
    # "Skill Description" : "Expert"
    # })
    

    # def authenticate_user(user : userLoginSchema):
    #     if check_user(user):
    #         return sign_JWT(user['username'])
    #     return {
    #         "ERROR" : "Invalid login details"
    #     }
    
    # test5 = authenticate_user({
    #     "username": "Kenneth",
    #     "password": "Surti"
    #     })
    #print(test1)
    #print(test2['msg'])
    #print(test3)
    #print(test4)
    #print(test5)
    #print(t.inserted_id) 
# except Exception as e:
#    print(e)


# print(client.list_database_names())
# print(db.list_collection_names())
