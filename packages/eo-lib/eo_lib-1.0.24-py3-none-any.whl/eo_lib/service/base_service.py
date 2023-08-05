from abc import ABC
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from eo_lib.config.config import engine
	
class BaseService(ABC):

    """ Abstract Class responsible for implemeting functions that are common in a service. """

    def __init__(self, object):
        self.object = object
        self.type = self.object.__tablename__
        self.create_session_connection()
    
    def close_session_connection(self):
        self.session.close()

    @contextmanager
    def create_session_connection(self):
        Session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False))
        self.session = Session()
        self.session.begin(subtransactions=True)
        try:
            yield self.session
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.expunge_all()
            self.session.close()


    def find_all(self):
        with self.create_session_connection() as session:   
            results = session.query(self.object).order_by(self.object.id).all()
            return results

    def find_by_uuid(self, uuid):
        with self.create_session_connection() as session:
        	return session.query(self.object).filter(self.object.uuid == uuid).first()
    
    def find_by_id (self, id):
    	with self.create_session_connection() as session:
    	     return session.query(self.object).get(id)

    def create(self, object):
        try:
            with self.create_session_connection() as session:     
            	local_object = self.session.merge(object)
            	self.session.add(local_object)
            	self.session.commit()
            	return local_object
        except:
            raise
    
    def create_bulk(self, list_object):
        try:
            with self.create_session_connection() as session:     
               	self.session.add_all(list_object)
               	self.session.commit()
               	return list_object
        except:
           raise

    def update(self, object):
        try:
            with self.create_session_connection() as session:
            	self.session.query(self.object).filter(self.object.id == object.id).update({column: getattr(object, column) for column in self.object.__table__.columns.keys()})
            	self.session.commit()
            	return object
        except:
            self.session.rollback() 
            raise

    def delete(self, object):
        try:
        	with self.create_session_connection() as session:
        	    self.session.delete(object)
        	    self.session.commit()	            	
        except:
            self.session.rollback() 
            raise

    def delete_by_uuid (self, uuid):
        try:
        	with self.create_session_connection() as session:
        	    self.session.query(self.object).filter(self.object.uuid == uuid).delete()
        	    self.session.commit()
        except:
            self.session.rollback() 
            raise

