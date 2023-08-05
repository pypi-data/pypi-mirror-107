from eo_lib.service.team.service import *
from eo_lib.application import factories as application_factory
from eo_lib.application.abstract_application import AbstractApplication

class PersonApplication(AbstractApplication):

    """ Application of  Person"""
    def __init__(self):
        super().__init__(PersonService())
		
    def to_dict(self, uuid):
        person = self.service.find_by_uuid(uuid)
        dict = person.to_dict()
        if person.role_id:
        	role_application = application_factory.RoleFactory()
        	role = role_application.find_by_id(person.role_id)
        	dict['role'] = role.to_dict() 
        return dict
	
class OrganizationApplication(AbstractApplication):

    """ Application of  Organization"""
    def __init__(self):
        super().__init__(OrganizationService())
		
    def to_dict(self, uuid):
        organization = self.service.find_by_uuid(uuid)
        dict = organization.to_dict()
        people_application = application_factory.Association_OrganizationPersonFactory()
        people = people_application.find_person_from_organization_all(organization.id)
        people_list = []
        if people:
           for person in people:
               people_list.append (person.to_dict())
        dict['people'] = people_list  
        return dict
	
class RoleApplication(AbstractApplication):

    """ Application of  Role"""
    def __init__(self):
        super().__init__(RoleService())
		
    def to_dict(self, uuid):
        role = self.service.find_by_uuid(uuid)
        dict = role.to_dict()
        return dict
	
