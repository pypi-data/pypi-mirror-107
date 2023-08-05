from eo_lib.config.config import Base
from sqlalchemy import Column ,ForeignKey, Integer
from sqlalchemy.orm import relationship

class Association_OrganizationPerson (Base):
    """Relationship between Organization and Person"""

    __tablename__ = 'organization_person'
    organization_id = Column(Integer, ForeignKey('organization.id'), primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    people = relationship("Person")


