import factory
from eo_lib.model.relationship.models import *
from eo_lib.model.team.models import *

class PersonFactory(factory.Factory):
    """ Factory of Model of Person """
    class Meta:
        model = Person

class OrganizationFactory(factory.Factory):
    """ Factory of Model of Organization """
    class Meta:
        model = Organization

class RoleFactory(factory.Factory):
    """ Factory of Model of Role """
    class Meta:
        model = Role

## Relationships
	
class Association_OrganizationPersonFactory(factory.Factory):
    """  of Organization """
    class Meta:
	    model = Association_OrganizationPerson
		
