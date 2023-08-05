from eo_lib.config.base import Entity
from sqlalchemy import Column, Boolean ,ForeignKey, Integer, DateTime, Date, String, Text
from sqlalchemy.orm import relationship
from eo_lib.model.relationship.models import *

class Person(Entity):
	
	"""A human Physical Agent."""
	
	is_instance_of = "person"
	__tablename__  = "person"
	serialize_only = ('name', 'index', 'description', )

	role_id = Column(Integer,ForeignKey('role.id'))

	

class Organization(Entity):
	
	"""A Organiztion"""
	
	is_instance_of = "organization"
	__tablename__  = "organization"
	serialize_only = ('name', 'index', 'description', )

	people = relationship("Association_OrganizationPerson")

	

class Role(Entity):
	
	"""A role played by a person in an organization """
	
	is_instance_of = "role"
	__tablename__  = "role"
	serialize_only = ('name', 'index', 'description', )


	
