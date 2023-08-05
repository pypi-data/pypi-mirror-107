import factory
from eo_lib.application.relationship.application import *
from eo_lib.application.team.application import *


class PersonFactory(factory.Factory):
    """ Factory of Application of Person """
    class Meta:
        model = PersonApplication


class OrganizationFactory(factory.Factory):
    """ Factory of Application of Organization """
    class Meta:
        model = OrganizationApplication


class RoleFactory(factory.Factory):
    """ Factory of Application of Role """
    class Meta:
        model = RoleApplication

## Relationships
class Association_OrganizationPersonFactory(factory.Factory):
     """Organization """
     class Meta:
          model = Association_OrganizationPersonApplication

			
	
