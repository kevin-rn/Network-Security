from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Session
import os

"""
This module is meant to setup/configure everything that is needed to interact with sqlite database using
SQLAlchemy library.
"""

SQLALCHEMY_ENGINE = "sqlite"
# creates db in current folder
SQLALCHEMY_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log_records.db")

"""
Engine is used by the session for connection resources and acts as a factory for db connections.

NOTE:
By default, check_same_thread is True and only the creating thread may use the connection.
If set False, the returned connection may be shared across multiple threads.
When using multiple threads with the same connection writing operations should be serialized by the user to 
avoid data corruption.

If it needs to be changed to False, also pass the following:
 connect_args = {"check_same_thread": False}
"""
engine = create_engine(
    f"{SQLALCHEMY_ENGINE}:///{SQLALCHEMY_DB_PATH}",
    connect_args={"check_same_thread": False},
    # echo=True,
)

"""
Scoped session used for all CRUD operations/database transactions.
"""
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

"""
SQLAlchemy does not know which entities we have created by default.
For this reason, we need to inherit each class with the declarative base class
So that SQLAlchemy knows how it needs to handle/map them during transactions.

Definition from docs:
Construct a base class for declarative class definitions.

The new base class will be given a metaclass that produces appropriate Table objects and 
makes the appropriate mapper() calls based on the information provided declaratively in the class and any subclasses of the class.
"""
Base = declarative_base()


"""
Context Manager for the database session.
A session manages persistence operations for ORM-mapped objects.
Scoped session is used for thread-safety.
NOTE: only 1 scoped session is re-used for each CRUD operation.
"""


class DbSession:
    def __init__(self):
        self.session = None

    def __enter__(self) -> Session:
        self.session = SessionLocal()
        return self.session

    def __exit__(self, type, value, traceback):
        # commit the changes in the session to the db.
        self.session.commit()
        self.session.close()

"""
Function to create tables of all defined classes that inherit from Base
(all those classes are contained in metadata by default)
checkfirst=True -> don't issue CREATEs for tables already present in the target database

IMPORTANT NOTE: make sure that all classes that inherit from the Base class are imported in the script
before calling `create_tables` function. OR import another module that import the classes.
If not, then the Base does not know about other classes and no tables will be created.
"""
create_tables = lambda: Base.metadata.create_all(bind=engine, checkfirst=True)
