from eo_lib.model.relationship.models import *
from eo_lib.model.team.models import *
from eo_lib.service.base_service import BaseService

class Association_OrganizationPersonService (BaseService):
    """Service of Relationship between Organization and Person"""

    def __init__(self):
    	super(Association_OrganizationPersonService, self).__init__(Association_OrganizationPerson)
    
    def find_person_from_organization_all(self,organization_id):
 	    with self.create_session_connection() as session:   
 	         return session.query(Person).join(Association_OrganizationPerson).filter(Person.id == Association_OrganizationPerson.person_id, Association_OrganizationPerson.organization_id == organization_id).all()
