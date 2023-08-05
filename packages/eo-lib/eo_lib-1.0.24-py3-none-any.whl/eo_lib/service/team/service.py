from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from eo_lib.model.team.models import *
from eo_lib.service.base_service import BaseService

class PersonService(BaseService):

    """ Service of Person"""

    def __init__(self):
        super(PersonService,self).__init__(Person)

class OrganizationService(BaseService):

    """ Service of Organization"""

    def __init__(self):
        super(OrganizationService,self).__init__(Organization)

class RoleService(BaseService):

    """ Service of Role"""

    def __init__(self):
        super(RoleService,self).__init__(Role)

