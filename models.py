import datetime
from pydantic import BaseModel
from typing import Union, List, Dict

def getCurrentDateParsed():
    current_date = datetime.datetime.now()
    parsed_date = f"{current_date.month}-{current_date.day}-{current_date.year} {current_date.hour}:{current_date.minute}"
    return parsed_date

class User(BaseModel):
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    email: str
    password: Union[str, None] = None
    new_password: Union[str, None] = None
    createdAt: str = getCurrentDateParsed()

class Token(BaseModel):
    token: str

class Company(BaseModel):
    name: str
    admin_user: str

class Company_User(BaseModel):
    name: str
    user_email: str

class Project(BaseModel):
    name: str
    admin_user: Union[str, None] = None
    launched: bool
    description: Union[str, None] = None
    parties: Union[List[Dict[str, Union[str, bool]]], None] = None
    createdAt: str = getCurrentDateParsed()

class ProjectID(BaseModel):
    project_id: str

class FundFlowActionReceive(BaseModel):
    project_id: str
    createdAt: str = getCurrentDateParsed()
    user_email: str
    first_name: str
    last_name: str
    data: Union[Dict[str, Union[str, int]], None] = None # this is a template for multiple information

class AddUserToProject(BaseModel):
    project_name: str
    first_name: str
    last_name: str
    user_email: str

class ProjectAudit(BaseModel):
    project_id: str
    first_name: str
    last_name: str
    source_use: str
    source_use_name: str
    source_use_amount: int
    createdAt: str = getCurrentDateParsed()