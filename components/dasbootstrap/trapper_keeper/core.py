from dasbootstrap.resources.paths import Directories
from sqlalchemy import Column, Integer, String, Unicode, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import engine

Base = declarative_base(bind=engine)
hosts_db = Directories.ANSIBLE_HOME

engine = create_engine()

class AnsibleHost(Base):
  __tablename__ = "hosts"
  id = Column(Integer, primary_key=True)
  name = Column(Unicode(63))
  address = Column(String(63))
