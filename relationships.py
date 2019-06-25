from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
import os
import sys
from datetime import datetime


engine = create_engine('sqlite:///db.sqlite3')
# Postgres Setup
# engine = create_engine(f'postgresql://{username}:{password}@{hostname}/{database}')

# Setup a session to the database (creating the empty database if it doesn't exist)
Session = sessionmaker(bind=engine) # Creates a new Session class binded to the engine for connections
session = Session() # Establishes a connection

# Create a new Base class for all declartive models
# to inherit from providng all the base functionality
# that each model requires
Base = declarative_base()

class Contact(Base):
    # Set the table name
    __tablename__ = 'contact'

    # Create individual table columns
    # including their types. 
    contact_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(DateTime, nullable=True)

    # Creates a class relationship (not part of the database itself)
    # that automatically finds all associated addresses when this is used. 
    # The back_populates fills the 'contact' field in the Address class whenever
    # a new instance is created. 
    addresses = relationship('Address', back_populates='contact')

    def __repr__(self):
        return (f'<Contact(contact_id={self.contact_id}, '
                f'first_name={self.first_name}, '
                f'last_name={self.last_name},'
                f'date_of_birth={self.date_of_birth})>')

class Address(Base):
    __tablename__ = 'address'

    address_id = Column(Integer, primary_key=True)
    apartment_number = Column(Integer, nullable=True)
    street_number = Column(Integer, nullable=False)
    street_name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    province = Column(String, nullable=False)

    
    # Configures the ForeignKey constraints - Ensuring that this record
    # cannot exist unless a contact exists and is assigned to this record. 
    contact_id = Column(Integer, ForeignKey('contact.contact_id'))
    
    # This creates a field 'contact' that will find the contact associated
    # with an instance of this class. The back_populates instructs the class
    # to load the 'addresses' field automatically in the Contact class.
    # The contact class needs this field created before this can actually
    # happen. 
    contact = relationship('Contact', back_populates='addresses')

# Using the base class create all the tables schemas
# in the memory database using the associated (inheriting)
# classes
Base.metadata.create_all(engine)

# Create a new contact with 2 addresses
contact = Contact(first_name='Russell', last_name='Yorke', date_of_birth=datetime(1982, 1, 4))
print(repr(contact.addresses)) # Notice this is an empty list at this moment
address_a = Address(street_number=191, street_name='Pioneer Ave', city='Winnipeg', province='Manitoba')
address_b = Address(street_number=166, street_name='Portage Ave E', city='Winnipeg', province='Manitoba')
contact.addresses.append(address_a)
contact.addresses.append(address_b)
print(repr(contact.addresses)) # Notice this list now holds entries

session.add(contact)
session.new # Notice this adds all three records with a single add

# Query for the record
contact = session.query(Contact).filter_by(first_name='Russell').one()
print(contact.first_name, contact.last_name)
for address in contact.addresses:
    print(address.street_number, address.street_name)