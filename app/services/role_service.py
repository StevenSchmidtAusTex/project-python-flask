from ..models import User, Role, db
from sqlalchemy.exc import IntegrityError
from datetime import datetime

# ISSUE IV build role_service.py

# def create_role(role_name, department_name)
# build new role object
# attempt to save to db
# ValueError if role with the same name exists
# return dict describing created role

# def assign_role_to_user(user_id, role_id)
# look up by user id / valueError
# look up by role id / valueError
# if user doesn't have role append it
# commit change
# return user info

# def list_roles()
# retrieve all roles in db
# query role objects
# sort by dept + role name
# convert to simple dictionary
# return the list

# def get_roles_for_user(user_id)
# retrieve all roles for specific user
# look up by user_id / valueError
# read user.roles relationship
# convert roles to dictionaries
# return list
