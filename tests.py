# import modules
import unittest
import sys

import mongo_functions
import models

# Documentation for testing
# For each different testing category set, a class will be created. It will inherit the unittest.TestCase
# class. Then, each different test we have for it will be a function of the class. Each function need to be
# named: test_ + the name we want. Then, we need to use the self.assert functions in order to fulfill the test
# requirement.

# Helper functions
# setUp(self) is used to create a set up that will be required in multiple test cases
# tearDown(self) is used to destroy or stop elements that needed to be closed at end of execution

# Assert functions
# self.assertEqual(hardCodedPart, givenByActualProgram) --> will pass the test if paramters are equal
# self.assertTrue(givenActualProgramValue) --> pass the test if returns true
# self.assertFalse(givenActualProgramValue) --> pass the test if returns false

# More documentation: https://docs.python.org/3/library/unittest.html

class TestDatabaseConnection(unittest.TestCase):

    def test_database_connection(self):
        mongo_functions.ConnectDB()

    def test_database_db_object(self):
        mongo_functions.GetDB("TestDB")

    def test_database_collection_object(self):
        mongo_functions.GetCollection("TestDB", "TestCollection")


class TestUserFunctions(unittest.TestCase):

    def test_a_insert_user(self):
        # create temporary user
        test_user = {"first_name": "temporal", "last_name": "user", "email": "temporal@user.com", "password": "123"}
        self.assertTrue(mongo_functions.InsertUser(test_user))

    def test_get_all_users(self):
        # get users
        test_users = mongo_functions.GetAllUsers()
        # check that it got at least one
        self.assertNotEqual(len(test_users), 0)

    def test_get_users_by_name(self):
        # get the temporal user that was inserted
        test_user = mongo_functions.GetUsersByName(first_name = "temporal", last_name = "user")
        # check that there is only one
        self.assertEqual(len(test_user), 1)

    def test_get_user_by_email(self):
        # get the user with email
        test_user = mongo_functions.GetUserByEmail("temporal@user.com")
        # check that it did not return false
        self.assertNotEqual(test_user, False)

    def test_z_delete_user_by_email(self):
        # delete the user
        test_user = mongo_functions.DeleteUserByEmail("temporal@user.com")
        self.assertTrue(test_user)

class TestCompanyFunctions(unittest.TestCase):

    def test_a_insert_company(self):
        # create test company
        test_company = {"name":"temporal_company"}
        # check that insertion was true
        self.assertTrue(mongo_functions.InsertCompany(test_company))

    def test_get_company_by_name(self):
        # get the temporal test company
        test_company = mongo_functions.GetCompanyByName(company_name="temporal_company")
        # check that there is only one company
        self.assertNotEqual(test_company, False)

    def test_z_delete_company(self):
        # delete company
        test_company = mongo_functions.DeleteCompanyByName("temporal_company")
        self.assertTrue(test_company)

class TestProjectFunctions(unittest.TestCase):

    def test_a_insert_project(self):
        # create test project
        test_project = {"name":"temporal_project", "admin_user":"temporal@user.com", "launched":"true", "createdAt":"Does not matter"}
        # check that insertion was true
        self.assertTrue(mongo_functions.InsertProject(test_project))

    def test_get_project_by_name(self):
        # get the temporal test project
        test_project = mongo_functions.GetProjectByName(project_name="temporal_project")
        # check that there is only one project
        self.assertNotEqual(test_project, False)
    
    def test_get_projects_by_admin_email(self):
        # get the projects by the temporal user
        projects = mongo_functions.GetAllProjectsByUser(email="temporal@user.com")
        # check that there is at least one project
        self.assertGreater(len(projects), 0)


    def test_z_delete_company(self):
        # delete company
        test_project = mongo_functions.DeleteProjectByName("temporal_project")
        self.assertTrue(test_project)

if __name__ == "__main__":
    unittest.main(verbosity=2)