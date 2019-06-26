from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, desc
from sqlalchemy.orm import sessionmaker
import os
import sys
from datetime import datetime

# Configure a DBAPI engine to manage the database
# interactions
# engine = create_engine('sqlite:///:memory:')
engine = create_engine('sqlite:///db.sqlite3', echo=True)
# engine = create_engine(f'postgresql://{username}:{password}@{hostname}/{database}')

# Create a active session manager using the DBAPI engine
Session = sessionmaker(bind=engine)
session = Session()

# Create a base class for managing all the databases
# that are of this type
Base = declarative_base()

class Contact(Base):
    # Map this class to the underlying database table
    __tablename__ = 'contact'

    # Map the individual database columns to fields
    # within this  class
    contact_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(DateTime, nullable=True)
    age = Column(Integer, default=18)

    def __repr__(self):
        # Output developer friendly string for  class
        return (f'<Contact(contact_id={self.contact_id}, '
                f'first_name={self.first_name}, '
                f'last_name={self.last_name},'
                f'date_of_birth={self.date_of_birth})>')


# Create any tables that don't already exist
Base.metadata.create_all(engine)

# Create a new record in the table
new_contact = Contact(first_name='Russell', last_name='Yorke', date_of_birth=datetime(1982, 1, 25))
print(repr(new_contact))

# add this record to the transaction list
session.add(new_contact)

# Add multiple contacts within a single transactions
session.add_all([
    Contact(first_name='Jane', last_name='Doe', date_of_birth=datetime(1985, 12, 24)),
    Contact(first_name='John', last_name='Doe', date_of_birth=datetime(1987, 4, 1)),
    Contact(first_name='Peter', last_name='Piper', date_of_birth=datetime(1992, 8, 1)),
    Contact(first_name='Jessica', last_name='Jones', date_of_birth=datetime(1992, 8, 1)),
    Contact(first_name='Mario', last_name='Zonka', date_of_birth=datetime(1992, 8, 1)),
    Contact(first_name='Luigi', last_name='Rodrigues', date_of_birth=datetime(1992, 8, 1)),
    Contact(first_name='Shane', last_name='Farris', date_of_birth=datetime(1992, 8, 1)),
    Contact(first_name='Evita', last_name='Cassella', date_of_birth=datetime(1992, 8, 1)),
    Contact(first_name='Emmie', last_name='Buchwald', date_of_birth=datetime(1992, 8, 1)),
    Contact(first_name='Dillion', last_name='Hamm', date_of_birth=datetime(1992, 8, 1)),
    Contact(first_name='Mitchell', last_name='Endres', date_of_birth=datetime(1992, 8, 1)),
    Contact(first_name='Chris', last_name='Smyers', date_of_birth=datetime(1992, 8, 1)),
])

# Show all records ready to be commited (saved) to the database
for record in session.new:
    print(repr(record))

# Commit the transaction (store in database)
session.commit()

# Update an existing record
new_contact.first_name = 'Jordan'

# Notice how the session knows this record has changed without having
# to add it to  the sessin?
for record in session.dirty:
    print(repr(record))

# Save the data updating the database
session.commit()

# Query the database for individual records
contacts = session.query(Contact).filter_by(first_name='Jordan', last_name='Yorke')
print(repr(contacts)) # Query set
print(repr(contacts.first()))

# Find all contacts
contacts = session.query(Contact).all()
print(f'Total contacts found: {len(contacts)}')
for contact in contacts:
    print(repr(contact))

# Few more operations stacking queries
contacts = session.query(Contact).limit(5).offset(5)
print(f'SQL Query: {contacts}')
contacts = contacts.all()
print(f'Total contacts returned: {len(contacts)}')
for contact in contacts:
    print(repr(contact))


# Query and order records in descending order by last name
contacts = session.query(Contact).order_by(desc(Contact.last_name))
print(f'Query for descending: {str(desc(Contact.last_name))}')
print(f'Total Contacts: {contacts.count()}')
for contact in contacts:
    print(repr(contact))

# Query for specific fields returns a tuple instead of a model
results = session.query(Contact.first_name, Contact.last_name)
print(type(results))
for first_name, last_name in results:
    print(f'{first_name} {last_name}')

# Filtering using operators
contacts = session.query(Contact).filter(Contact.last_name == 'Yorke').all()
print(f'Total contacts found: {len(contacts)}')
for contact in contacts:
    print(repr(contact))
contacts = session.query(Contact).filter(Contact.contact_id >= 3).all()
print(f'Total contacts found: {len(contacts)}')
for contact in contacts:
    print(repr(contact))
contacts = session.query(Contact).filter(Contact.last_name.like('%orke')).all()
print(f'Total contacts found: {len(contacts)}')
for contact in contacts:
    print(repr(contact))

# Deleting a contact
contacts = session.query(Contact).filter(Contact.first_name.ilike('Jane')).all()
print(f'Found {len(contacts)} contacts to delete')
for contact in contacts:
    session.delete(contact)
session.commit()


# Automatic error checking
try:
    invalid_contact = Contact(first_name=1, last_name=1, date_of_birth=1, age="hello")
    session.add(invalid_contact)
    session.commit()
except Exception as e:
    print(e)