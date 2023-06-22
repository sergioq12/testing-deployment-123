# This is a file where all database functionality will be hold. 
# MongoDB is the database we are currently using, therefore pymongo library will be used as ORM
# in order to access and make mongoDB queries. The functions that will be created will have documentation
# stating there actions. For each function, a unittest will be created.

# Functions and what they do:

# Connection, DB, and Collection retrieval
# pymongo.MongoClient(DB_URL) --> Connects to DB with the correct url
# pymongo.MongoClient(DB_URL)[db_name] --> Connects to DB and gets the DB with the name given
# pymongo.MongoClient(DB_URL)[db_name][collection_name] --> Connects to DB and gets the collection from the given collection name that should be under the given db name

# Inserting elements
# collection.insert_one(object) --> Inserts one object given into the collection that has been chosen
# collection.insert_many(List[object]) --> Inserts every objects given in a list into the collection that has been chosen

# Queries and Getting elements
# collection.find({key_name: value}) --> Gets all occurrences of objects that have the corresponding condition given in the argument
# collection.find_one({key_name: value}) --> Gets only the user that has the corresponding condition given in the argument. If there are multiple, it will retrieve the first instance

# Update Elements
# collection.update_one({key_name: value_condition}, {"$set":{key_name: intended_value}}) --> Updating does a query search with the first JSON object passed. Then it changes the corresponding key to a new value given, the intended one
# collection.update({key_name: value_condition}, {"$set":{key_name: intended_value}}) --> Does the same above but for all values matching the corresponding condition

# Delete Elements
# collection.delete_one({key_name: value}) --> Deletes the object that corresponds to the condition given. If there are multiple, it will delete the first instance that was added to the collection
# collection.delete_mane({key_name: value}) --> Deletes all object instances that have a match with the condition given within the collection


import pymongo
import os
from dotenv import load_dotenv
from bson import ObjectId

# Loads environment variables (once we deploy this app we need to switch to github secrets or GCP hidden values)
load_dotenv()

# DB Connection functions
def ConnectDB():
    """
    This function will use pymongo.MongoClient to connect to the database using the DB url given in the .env file.
    It will return a client that can be used to access each DB from each DB each collection can be accessed
    """
    client = pymongo.MongoClient(os.getenv("MONGODB_URL"))
    return client
    
def GetDB(db_name):
    """
    This function will make the connection with the pymongo client and it will retrieve a database with the name given.
    """
    client = ConnectDB()
    return client[db_name]

def GetCollection(collection_name, db_name):
    """
    This function will make the connection with the pymongo client and it will retrieve a collection with the name given.
    """
    client = ConnectDB()
    return client[db_name][collection_name]


# DB Required Functions

# User Functions

def InsertUser(user):
    """
    This function will insert the user given in the parameter. It is important that the user is a Pydantic model, 
    so that we can then turn it into a dictionary that can be given to the database

    User in argument entered is a dictionary already

    """

    # connect with the collection
    collection = GetCollection("Users", "Syndagent")
    # insert the user dictionary
    try:
        collection.insert_one(user)
        print("A user has been inserted")
        return True
    except:
        return False


def GetAllUsers():
    """
    This function will do a query to retrieve all users from the database and return them in a list of objects 
    """
    # Connect to User collection
    collection = GetCollection("Users", "Syndagent")

    # get all users
    users = collection.find()
    users_list = []
    for user in users:
        users_list.append(user)
    return users_list

def GetUsersByName(first_name, last_name):
    """
    This function will take a username as a parameter and it will retrieve the user with the corresponding username.
    """
    # connect to collection
    collection = GetCollection("Users", "Syndagent")

    # try to find users with the given name
    users = collection.find({"first_name": first_name, "last_name": last_name})
    users_list = []
    for user in users:
        users_list.append(user)
    return users_list

def GetUserByEmail(email):
    """
    This function will take a email as a parameter and it will retrieve the user with the corresponding email.
    """
    # connect to collection
    collection = GetCollection("Users", "Syndagent")

    # get user by its email
    try:
        user = collection.find_one({"email": email})
        return user
    except:
        return False


def GetUserByPhoneNumber(phone_number):
    """
    This function will take a phone number as a parameter and it will retrieve the user with the corresponding number.
    """
    pass

def GetUsersByProject(project_name):
    """
    This function will take a project name as a parameter and it will find the project object by its name. 
    Then it will find the users that are linked to the corresponding project.
    """
    pass

def GetUsersByCompany(company_name):
    """
    This function will take a company name as a parameter and it will find the company object by its name. 
    Then it will find the users that are linked to the corresponding company.
    """
    pass

def DeleteUserByEmail(email):
    """
    This function will delete an user from the database given the email.
    """
    # connect to the collection
    collection = GetCollection("Users", "Syndagent")

    # delete the user
    try:
        user_deleted = collection.delete_one({"email": email})
        print(user_deleted)
        print("A user has been deleted")
        return True
    except:
        return False


# Project Functions

def InsertProject(project):
    """
    This function will obtain a project object and add it to the database. Return true if added
    successfully or false if there was an issue.
    
    Project in argument entered is a dictionary already
    """

    # connect with the collection
    collection = GetCollection("Project", "Syndagent")
    # insert the project dictionary
    try:
        collection.insert_one(project)
        print("A project has been inserted")
        return True
    except:
        return False

def GetProjectById(project_id):
    """
    This function will get a project with its ID. The idea is to obtain the data of the project
    """
    # connect with the collection
    collection = GetCollection("Project", "Syndagent")
    project = collection.find_one({"_id":ObjectId(project_id)})
    project_id = str(project["_id"])
    new_project = {
            "name":project["name"],
            "launched": project["launched"],
            "createdAt": project["createdAt"],
            "project_id": project_id
        }
    if new_project:
        return new_project
    else:
        return False

def GetAllProjects():
    """
    This function will retrieve all projects from the database and returns them as a list of objects
    """
    pass

def GetAllProjectsByUser(email):
    """
    This will get all projects where the user email is the admin email. 
    """
    # connect with collectioin 
    collection = GetCollection("Project", "Syndagent")
    
    # get all projects
    projects = collection.find({"admin_user": email})
    new_projects = []
    for project in projects:
        project_id = str(project["_id"])
        new_project = {
            "name":project["name"],
            "launched": project["launched"],
            "createdAt": project["createdAt"],
            "project_id": project_id
        }
        new_projects.append(new_project)
    return new_projects


def GetProjectByName(project_name):
    """
    This function will retrieve a project object by the name given.
    If no project is found, then it should raise a ProjectNotFound exception.
    """
    # connect to collection
    collection = GetCollection("Project", "Syndagent")

    # get company by its name
    try:
        project = collection.find_one({"name": project_name})
        return project
    except:
        return False

def GetProjectsByCompany(company_name):
    """
    This function will retrieve the company object with the company name and then it will retrieve all projects that 
    are worked by an specific company. It should return a list of project objects.
    If no project is found, then it should raise a ProjectNotFound exception.
    """
    pass

def GetProjectAuditsByProjectName(project_name):
    """
    This function will retrieve all the audits that are linked to the project object.
    If no audits are found, then it should raise a AuditNotFound exception.
    """
    pass

def GetProjectsByCompanyCreatedFromDate(company_name, date):
    """
    This function will retrieve all projects from a company from a specific date to the actual date. 
    If no project is found, then it should raise a ProjectNotFound exception.
    """
    pass

def DeleteProjectByName(name):
    """
    This function will delete a project from the database given the name.
    """
    # connect to the collection
    collection = GetCollection("Project", "Syndagent")

    # delete the user
    try:
        project_deleted = collection.delete_one({"name": name})
        print(project_deleted)
        print("A Project has been deleted")
        return True
    except:
        return False


# Company Functions

def InsertCompany(company):
    """
    This function will obtain a company object and add it to the database. Return true if added
    successfully or false if there was an issue.
    
    Company in argument is a dictionary already
    """

    # connect with the collection
    collection = GetCollection("Company", "Syndagent")
    # insert the company dictionary
    try:
        collection.insert_one(company)
        print("A Company has been inserted")
        return True
    except:
        return False

def GetAllCompanies():
    """
    This function will retrieve all companies that are find in the database and returns them in a list of company objects
    """
    pass

def GetCompanyByName(company_name):
    """
    This function will retrieve the company object that is found under the company name given.
    If no company is found then a CompanyNotFound exception should be raised.
    """
    # connect to collection
    collection = GetCollection("Company", "Syndagent")

    # get company by its name
    try:
        user = collection.find_one({"name": company_name})
        return user
    except:
        return False
    
def DeleteCompanyByName(name):
    """
    This function will delete a company from the database given the name.
    """
    # connect to the collection
    collection = GetCollection("Company", "Syndagent")

    # delete the user
    try:
        company_deleted = collection.delete_one({"name": name})
        print(company_deleted)
        print("A company has been deleted")
        return True
    except:
        return False

def GetCompanyByUserEmail(user_email):
    """
    This function will find a company by its user_email.
    """
    # connect to the collection
    collection = GetCollection("Company_User", "Syndagent")
    try:
        company_user = collection.find_one({"user_email": user_email})
        return company_user["company_name"]
    except:
        print("Something occured")
        

# Company-User Functions

def InsertCompanyUser(company_user):
    """
    This function will obtain a company_user object and add it to the database. Return true if added
    successfully or false if there was an issue.
    
    Company_user argument entered is a dictionary already
    """

    # connect with the collection
    collection = GetCollection("Company_User", "Syndagent")
    # insert the company_user dictionary
    try:
        collection.insert_one(company_user)
        print("A company_user element has been inserted")
        return True
    except:
        return False

# Audit Functions

def GetAllAudits():
    """
    This function will retrieve all audit objects that are in the collection.
    """
    pass

def GetAuditByDate(date):
    """
    This function will retrieve all the audits that happened in the date given.
    If not audits are found, then it should raise an AuditNotFound exception.
    """
    pass


# Fund Flow Functions

def InsertFundFlowAction(fund_flow_action):
    """
    This function will get a fund flow action dictionary and it will insert it into mongo db.
    *** There are still updates needed after meeting with Jarrod
    """

    # connect with the collection
    collection = GetCollection("Fund Flow Action", "Syndagent")
    # insert the company dictionary
    try:
        collection.insert_one(fund_flow_action)
        print("A Fund Flow Action has been inserted")
        return True
    except:
        return False

def GetFundFlowActionsByProjectID(project_id):
    """
    This function will get all the fund flow actions that are under the project id
    given in the parameter.
    """
    # connect with the collection
    collection = GetCollection("Fund Flow Action", "Syndagent")

    # get the fund flow action
    try:
        fundFlowActions = collection.find({"project_id": project_id})
        fundFlowActionsList = []
        for action in fundFlowActions:
            # the project id is being passed, therefore its already known
            # hashtag get rid of redundancy
            del action["project_id"]
            action["_id"] = str(action["_id"])
            fundFlowActionsList.append(action)
        return fundFlowActionsList
    except:
        return False

# Audit Functions
def InsertAudit(audit):
    """
    This function will get a audits dictionary and it will insert it into mongo db.
    *** There are still updates needed after meeting with Jarrod
    """

    # connect with the collection
    collection = GetCollection("Audit", "Syndagent")
    # insert the company dictionary
    try:
        collection.insert_one(audit)
        print("An audit has been inserted")
        return True
    except:
        return False

def GetAuditsByProjectID(project_id):
    """
    This function will get all the audits that are under the project id
    given in the parameter.
    """
    # connect with the collection
    collection = GetCollection("Audit", "Syndagent")

    # get the fund flow action
    try:
        audits = collection.find({"project_id": project_id})
        auditList = []
        for audit in audits:
            # the project id is being passed, therefore its already known
            # hashtag get rid of redundancy
            del audit["project_id"]
            audit["_id"] = str(audit["_id"])
            auditList.append(audit)
        return auditList
    except:
        return False