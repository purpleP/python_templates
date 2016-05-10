from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite://')
engine.execute("attach database ':memory:' as db1;")
engine.execute("attach database ':memory:' as db2;")
Base = declarative_base()
session = sessionmaker(bind=engine)()


class Foo(Base):
    __tablename__ = 'foos'
    __table_args__ = {'schema': 'db1'}
    id = Column(String, primary_key=True)
    bars = relationship('Bar', uselist=True)


class Bar(Base):
    __tablename__ = 'bars'
    __table_args__ = {'schema': 'db1'}
    id = Column(String, primary_key=True)
    foo_id = Column(String, ForeignKey('db1.foos.id'))    
    baz_id = Column(String, ForeignKey('db2.bars.id'))
    
    
class Baz(Base):
    __tablename__ = 'bars'
    __table_args__ = {'schema': 'db2'}   
    id = Column(String, primary_key=True)
    bars = relationship('Bar', uselist=True)

    
Base.metadata.create_all(engine)