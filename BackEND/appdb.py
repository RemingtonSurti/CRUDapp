import os
import pymongo
from bson import ObjectId
import pprint
import datetime
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

KEY = os.environ.get("Mongo_KEY")
PASSWORD = os.environ.get("Mongo_PWD") 

connection_string = f"mongodb+srv://mongodb:{PASSWORD}@trainingdb.c92yljh.mongodb.net/?retryWrites=true&w=majority&authSource=admin"


client = pymongo.MongoClient(connection_string) 
db = client.EmployeeDB




users = db['Users']
def create_user():
    users_validator = {
        "$jsonSchema" : {
           "bsonType" : "object",
            "required" : ["Username","Password"],
            "properties" :{
                "Username" : {
                    "bsonType" : "string",
                    "description" : "Must be a unique not null string"
                    },
                "Password" : {
                    "bsonType" : "string",
                    "description" : "cannot be empty"
                    }
                }
            }
        }

    db.command("collMod", "Users", validator = users_validator)

#try:
#    db.create_collection("Users")
#except Exception as e:
#    print(e)

#create_user()



employees = db['Employees']
def create_employee():
    employees_validator={
        "$jsonSchema" : {
            "bsonType" : "object",
            "required" : ["First Name","Last Name","DOB","Email", "Skill Level","Active","Age"],
            "properties" :{
                "First Name" : {
                    "bsonType" : "string",
                    "description" : "Must be a unique not null string"
                    },
                "Last Name" : {
                    "bsonType" : "string",
                    "description" : "Must be a unique not null string"
                    },
                "DOB" : {
                    "bsonType" : "date",
                    "description" : "Must be a unique not null string"
                    },
                "Email" : {
                    "bsonType" : "string",
                    "description" : "Must be a unique not null string"
                    },
                "Skill Level" : {
                    "bsonType" : "array",
                    "description" : "This object should contain the skill of the employee"
                    },
                "Active" : {
                    "bsonType" : "bool",
                    "description" : "Must be a not null boolean"
                    },
                "Age" : {
                    "bsonType" : "int",
                    "minimum" : 18,
                    "description" : "Must be a not null integer greater than 18"
                    }
                }
            }
        }
    db.command("collMod", "Employees", validator = employees_validator)

# try:
#     db.create_collection("Employees")
# except Exception as e:
#     print(e)


# create_employee()


skill_level = db['Skill Levels']
def add_skill():
    skill_validator={
        "$jsonSchema" : {
            "bsonType" : "object",
            "required" : ["Skill Name","Skill Description"],
            "properties" :{
                "Skill Name" : {
                    "bsonType" : "string",
                    "description" : "Must be a unique not null string"
                    },
                "Skill Description" : {
                    "bsonType" : "string",
                    "enum" : ["Beginner","Intermediate","Advanced","Expert"],
                    "description" : "Must be a not null string Beginner,Intermediate,Advanced or Expert",
                    }
                }
            }
        }
    db.command("collMod", "Skill Levels", validator = skill_validator)



#try:
#    db.create_collection("Skill Levels")
#except Exception as e:
#    print(e)

#add_skill()

#db.command("collMod", "Skill Levels", validator = skill_validator)
skill_level_object = skill_level.find_one({ "$and" : [{"Skill Name":"Python"},{"Skill Description":"Expert"}]})
skill_level_id = str(skill_level_object['_id'])
skill_name=skill_level_object['Skill Name']
skill_description=skill_level_object['Skill Description']
admin_dict_employees={
    "First Name" : "admin",
    "Last Name" : "admin",
    "DOB" : datetime.datetime(1997, 12, 24),
    "Email" : "remosurti@gmail.com",
    "Skill Level" : [{
        "Skill Level ID" : skill_level_id,
        "Skill Name" : skill_name,
        "Skill Description" : skill_description
    }],
    "Active" : True,
    "Age": 24
}

admin_dict_skill={
    "Skill Name" : "Python",
    "Skill Description" : "Beginner"
}


admin_dict={
    "Username" : "Remo",
    "Password" : "Remo"
}

# try:
#     #users.insert_one(admin_dict)
#     employees.insert_one(admin_dict_employees)
#     #skill_level.insert_one(admin_dict_skill)
# except Exception as e:
#     print(e)

print(client.list_database_names())

#print(datetime.datetime.today())

#skill_level.update_one({"_id" : _id},{"$set"} : {"Skill Name" : })