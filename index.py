# Getting started lets gooo
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bcrypt import gensalt, hashpw, checkpw
from models import *
import jwt
import os
from dotenv import load_dotenv
import sys
import datetime
import mongo_functions
import hashlib
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Loads 
load_dotenv()

# Creates FastAPI app
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000/",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[*],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def test_endpoint():
    return {"message": "This is the main test"}

@app.get("/testing")
async def Testing():
    """
    This is a testing endpoint that allows us to know if the API is 
    giving out responses to the corresponding call
    """
    print("Testing endpoint")
    return {
        "Status":"Success",
        "Message": "This is a testing function, it works SIUUU"
    }

# User Authentication

@app.post("/sign_in")
async def SignIn(user: User):
    """
    This is the sign in endpoint. It will receive a user and it will
    verify that the email exists, and that the password matches. It will
    give according responses to given events
    """
    print("Sign in endpoint")
    # verify that the user email does exists 
    user_in_db = mongo_functions.GetUserByEmail(user.email)
    if user_in_db:
        # verify that the passwords match
        if checkpw(user.password.encode(), user_in_db["password"]):
            # Generate JWT 
            jwt_token = jwt.encode({
                "first_name": user_in_db["first_name"],
                "last_name": user_in_db["last_name"],
                "email": user.email,
                "date": str(user.createdAt)
            }, os.getenv("JWT_KEY"), algorithm='HS256')
            return {
                "Status": "Success",
                "Message": "User signed in successfully",
                "token": jwt_token
            }
        else:
            return {
                "Status": "Failure",
                "Message": "Passwords did not match"
            }
        
    else:
        # given that the email does not exist, can't authenticate
        return {
            "Status": "Failure",
            "Message": "Email was not found"
        }


# TODO: We should probably add a Sign-Up Verification Email here using Sendgrid. Can integrate with this endpoint.
@app.post("/sign_up")
async def SignUp(user: User):
    """
    This is the sign up endpoint. It will verify that the user given has a new
    email that has not been used. It will add the user to the database.
    It will return responses according to given events
    """
    print("Sign up endpoint")
    # verify that the user email does not exists 
    if mongo_functions.GetUserByEmail(user.email):
        # given that the email is taken, give a failure response
        return {
            "Status": "Failure",
            "Message": "Email was already taken"
        }
    else:
        # email is not taken, check that there is:
            # first and last name are given
        if user.first_name is not None and user.last_name is not None:
            # hash password using bcrypt
            salt = gensalt()
            user.password = hashpw(user.password.encode(), salt)
            
            # This builds object with info that database only needs
            user_for_db = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "password": user.password,
                "createdAt": user.createdAt
            }
            # add user to DB
            if mongo_functions.InsertUser(user_for_db) == False:
                return {
                    "Status": "Failure",
                    "Message": "Internal Inserting user error occured"
                }

            # Generate JWT 
            jwt_token = jwt.encode({
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "date": str(user.createdAt)
            }, os.getenv("JWT_KEY"), algorithm='HS256')
            return {
                "Status":"Success",
                "Message": "User signed up successfully",
                "token": jwt_token
            }
        else:
            # as information is missing return negative response
            return {
                "Status": "Failure",
                "Message": "Name was not given correctly"
            }

@app.post("/get_info")
async def getUserInfo(token: Token):
    try: 
        # generate JWT 
        decoded_message = jwt.decode(token.token, os.getenv("JWT_KEY"), algorithms=["HS256"])
        return {
            "status":"Success",
            "data":decoded_message
        }
    except:
        return {
            "status": "Failure",
            "message": "Token was not valid"
        }

# Company Routes

@app.post("/add_company")
async def addCompany(company: Company):
    company_dict = company.dict()
    # verify is company is already created
    if mongo_functions.GetCompanyByName(company_dict["name"]):
        return {
            "Status":"Failure",
            "Message": "Company name is already taken"
        }
    else:
        # add company to db
        try:
            mongo_functions.InsertCompany(company_dict)
            return {
                "Status":"Success",
                "message": f"{company_dict['name']} has been inserted to db"
            }
        except Exception as e:
            return {
                "Status":"Failure",
                "Message": e.message
            }

# Project Routes

@app.post("/add_project")
async def addProject(project: Project):
    project_dict = project.dict()
    # verify that project name is available
    if mongo_functions.GetProjectByName(project_dict["name"]):
        return {
            "Status": "Failure",
            "Message":"Project with given name is already taken"
        }
    else:
        # add project to db
        try:
            mongo_functions.InsertProject(project_dict)
            for party in project_dict["parties"]: # Send emails to invited parties
                userToAdd: AddUserToProject = AddUserToProject(
                    project_name=project_dict["name"],
                    first_name=party["first_name"],
                    last_name=party["last_name"],
                    user_email=party["email"]
                )
                await inviteUserToProject(userToAdd)
            return {
                "Status":"Success",
                "message": f"{project_dict['name']} has been inserted to db"
            }
        except Exception as e:
            return {
                "Status":"Failure",
                "Message": e.message
            }
        
@app.post("/get_projects_by_user")
async def getProjectsByUser(user: User):
    user_dict = user.dict()
    if mongo_functions.GetUserByEmail(user_dict["email"]):
        # given that the email exists in the db, then get the projects by the user
        projects = mongo_functions.GetAllProjectsByUser(user_dict["email"])
        return {
            "Status":"Success",
            "projects":projects
        }
        
    else:
        return {
            "Status": "Failure",
            "Message": "User is not in db"
        }

@app.post("/get_project_by_id")
async def getProjectById(project_id: ProjectID):
    project_id_str = project_id.dict()["project_id"]
    # Get project information
    project = mongo_functions.GetProjectById(project_id_str)
    if project:
        return {
            "Status":"Success",
            "project": project
        }
    else:
        return {
            "Status": "Failure",
            "message": "Something went wrong trying to find the project by id"
        }
    
# Fund Flow Routes

@app.post("/send_fund_flow")
async def sendFundFlowAction(fundFlow: FundFlowActionReceive):
    fundFlowAction = fundFlow.dict()
    print(fundFlowAction)

    # NOTE: This can be optimized by having the company and project_id
    # in the global state of the app and being passed as info in the request

    # with the user_email, get the company of the project
    company_name = mongo_functions.GetCompanyByUserEmail(fundFlowAction["user_email"])

    # create object and send it to mongodb under the table Fund Flow Actions
    fundFlowObject = {
        "company_name": company_name,
        "project_id": fundFlowAction["project_id"],
        "user_email": fundFlowAction["user_email"],
        "first_name": fundFlowAction["first_name"],
        "last_name": fundFlowAction["last_name"],
        "data": fundFlowAction["data"],
        "createdAt": fundFlowAction["createdAt"],
    }

    # inserting it to db
    try:
        if mongo_functions.InsertFundFlowAction(fundFlowObject):
            return {
                "Status": "Success",
                "Message": "Fund Flow succesfully added to db"
            }
        raise Exception
    except Exception as e:
        return {
            "Status": "Failure",
            "Message": f"Something went wrong, error message: {e.message}"
        }
    # create object and send it to mongodb under the table Audit
    
@app.post("/get_fund_flow_by_project_id")  
async def GetFundFlowsByProjectId(project_id: ProjectID):
    project_id_str = project_id.dict()["project_id"]
    # Get fund flow actions by project id
    fundFlowActions = mongo_functions.GetFundFlowActionsByProjectID(project_id_str)
    if fundFlowActions != False:
        return {
            "status": "Success",
            "data": fundFlowActions
        }
    else:
        return {
            "status": "Failure",
            "message": "Something went wrong with getting the fund flow actions"
        }

"""
Sendgrid Imports
"""

"""
This endpoint is user to invite a user to a project in Syndagent. This will trigger an
invite sent via email with Sengrid
"""
@app.post("/invite_user_to_project")
async def inviteUserToProject(addUser: AddUserToProject): # Trying to test without parameters first
    addUser = addUser.dict()
    print(addUser)
    To_Email = str(addUser["user_email"])
    Subject = str(addUser["first_name"])+', you have been invited to collaborate on '+str(addUser["project_name"])+'in Syndagent'
    message = Mail(
        from_email='jarrodstebick@gmail.com', # Both emails need to be set to legitimate emails for testing.
        to_emails=To_Email,
        subject=Subject,
        html_content='Successfully Sent Message Via Syndagent!')
    try:
        # userToAdd = addUser.dict()
        # print(userToAdd)
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return {
            "Status":"Success",
            "Message":"Email Sent!"
        }
    except Exception as e:
        # print(e.message)
        print('Error')
        return {
            "Status":"Failure",
        }

"""
This endpoints records Audits for a project.
"""
@app.post("/record_project_audit")
async def recordProjectAudit(projectAudit: ProjectAudit):
    try:
        auditString = str(projectAudit.first_name) + " " + str(projectAudit.last_name) + " added " + str(projectAudit.source_use_name) + " as a "
        if str(projectAudit.source_use) == "source":
            auditString += "source"
        elif str(projectAudit.source_use) == "use":
            auditString += "use"
        auditString += " in the amount of " + str(projectAudit.source_use_amount)+"."

        audit = {
            "project_id": projectAudit.project_id,
            "description": auditString,
            "createdAt": projectAudit.createdAt
        }
        if mongo_functions.InsertAudit(audit):
            return {
                "status":"Success",
                "Message":auditString
            }
        else:
            raise Exception
    except:
        return {
            "status":"Failure",
            "Message":"Error adding audit to project"
        }

@app.post("/get_audits_by_project_id")  
async def GetAuditsByProjectId(project_id: ProjectID):
    project_id_str = project_id.dict()["project_id"]
    # Get fund flow actions by project id
    audits = mongo_functions.GetAuditsByProjectID(project_id_str)
    if audits != False:
        return {
            "status": "Success",
            "data": audits
        }
    else:
        return {
            "status": "Failure",
            "message": "Something went wrong with the audit retrieval"
        }

