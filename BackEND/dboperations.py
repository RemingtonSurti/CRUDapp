import pymongo
from bson import ObjectId
import datetime
from BackEND.model import userLoginSchema, getemployeeSchema
from decouple import config
from werkzeug.security import generate_password_hash, check_password_hash




connection_string = f"mongodb+srv://mongodb:{config('Mongo_PWD')}@trainingdb.c92yljh.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
client = pymongo.MongoClient(connection_string) 
db = client.EmployeeDB

users = db['Users']
employees = db['Employees']
skill_level = db['Skill Levels']

admin_dict={
    "Username" : "Cristiano",
    "Password" : generate_password_hash("Ronaldo", method='sha256')
}

admin_dict_skill={
    "Skill Name" : "Python",
    "Skill Description" : "Advanced"
}

# try:
#     users.insert_one(admin_dict)
#     #employees.insert_one(admin_dict_employees)
#     #skill_level.insert_one(admin_dict_skill)
# except Exception as e:
#    print(e)

def get_skill(skillname : str, skilldescription : str) -> object:
    try:
        skill_level_object = skill_level.find_one({"$and": [{"Skill Name":skillname}, {"Skill Description" : skilldescription}]})
        skill_level_id = str(skill_level_object['_id'])
        return {
            "Skill Level ID" : skill_level_id,
            "Skill Name" : skillname,
            "Skill Description" : skilldescription
        }
    except Exception as e:
        print(e)

def get_employee(employee_ID : ObjectId) -> object:
    try:
        employee_object = employees.find_one({"_id" : employee_ID})
        ep_firstname = str(employee_object['First Name'])
        ep_lastname = str(employee_object['Last Name'])
        return {
            "firstname" : ep_firstname,
            "lastname" : ep_lastname
        }
    except Exception as e:
        print(e)

def checkToAdd_user_pass(user : userLoginSchema) -> object:
    try:
        data = users.find()
        for doc in data:
            if doc['Username'] == user['username']:
                if check_password_hash(doc["Password"],user["password"]):
                    return {"msg" : "Username or password already exists"}
                else:
                    users.insert_one({
                        "Username" : user['username'],
                        "Password" : user['password'] 
                    })
        return {"msg" :"User added Successfully"}
    except Exception as e:
        print(e)

def checkToAdd_emp(emp : getemployeeSchema) -> object:
        l = employees.find_one({ "$or" : [{"First Name" : emp['firstname']}, {"Email" : emp['email']}]})
        add_emp = {
                "First Name" : emp['firstname'],
                "Last Name" : emp['lastname'],
                "DOB" : datetime(emp['yr'], emp['mon'], emp['day']),
                "Email" : emp['email'],
                "Skill Level" : [get_skill(emp['skill_name'], emp['skill_description'])],
                "Active" : emp['Active'],
                "Age": emp['Age']
            }
        if l:
            return {"ERROR" : "Employee already exists"}
        else:
            #doc = employees.insert_one(add_emp)
            return {
                "msg":"Employee added Successfully"
                }
            


def checkToAdd_skill(skill : skill_level) -> str:
    try:
        l = skill_level.find_one({ "$and" : [{"Skill Name" : skill['Skill Name']}, {"Skill Description" : skill['Skill Description']}]})
        if l:
            return "Skill already exists"
        else:
            skill_level.insert_one({
                "Skill Name" : skill['Skill Name'],
                "Skill Description" : skill['Skill Description']
                })
            return "New Skill added Successfully"
    except Exception as e:
        print(e)

def check_user(data : str):
    try:
        l = users.find_one({"Username" : data})
        if l:
            return l
        return {"msg" : "Invalid user datails"}, 401
    except Exception as e:
        print(e) 

    
     


try:
    #encrypter = Fernet(encrypt_key)
    #test = get_skill("Python", "Advanced")
    #test1 = get_employee(ObjectId('63a606bb85815fba95cc588c'))
    # x = users.find_one({"Username" : "Cristiano"})
    # print(x)
    # print(check_password_hash(x['Password'], "Ronaldo"))
    # test2 = checkToAdd_user_pass({
    #     "Username" : x['Username'],
    #     "Password" : check_password_hash(x['Password'], "Ronaldo")
    # })
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

    t = "abc"

    # users.insert_one({
    #             "Username" : t,
    #             "Password" : encrypter.encrypt(t.encode())
    #             })
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
    # "Skill Name" : "Python",
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
    #print(test2)
    #print(test3)
    #print(test4)
    #print(test5) 
except Exception as e:
   print(e)


# print(client.list_database_names())
# print(db.list_collection_names())
