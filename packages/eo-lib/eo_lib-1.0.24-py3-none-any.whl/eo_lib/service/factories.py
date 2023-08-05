import factory
from eo_lib.service.relationship.service import *
from eo_lib.service.team.service import *

class PersonFactory(factory.Factory):
    """ Factory of Service of Person """
    class Meta:
        model = PersonService

class OrganizationFactory(factory.Factory):
    """ Factory of Service of Organization """
    class Meta:
        model = OrganizationService

class RoleFactory(factory.Factory):
    """ Factory of Service of Role """
    class Meta:
        model = RoleService

## Relationships
	
class Association_OrganizationPersonServiceFactory(factory.Factory):
    """ Service of Organization """
    class Meta:
	    model = Association_OrganizationPersonService
	
