from eo_lib.application.abstract_application import AbstractApplication
from eo_lib.service.relationship.service import *


class Association_OrganizationPersonApplication(AbstractApplication):
    """Application of Relationship between Organization and Person"""

    def __init__(self):
    	super().__init__(Association_OrganizationPersonService())
    
    def find_person_from_organization_all(self,organization_id):
 	    return self.service.find_person_from_organization_all(organization_id)
