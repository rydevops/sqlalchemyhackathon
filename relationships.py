from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
import os
import sys
from datetime import datetime

Base = declarative_base()

contact_person_number_table = Table('contact_person_number', 
                                    Base.metadata,
                                    Column('contact_id', Integer, ForeignKey('contact.contact_id')),
                                    Column('phone_number_id', Integer, ForeignKey('phone_number.phone_number_id')))

class Contact(Base):
    __tablename__ = 'contact'

    contact_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(DateTime, nullable=True)

    addresses = relationship('Address', back_populates='contact')
    email_addresses  =  relationship('EmailAddress', back_populates='contact')
    phone_numbers  = relationship('PhoneNumber', 
                                  secondary=contact_person_number_table)

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

    contact_id = Column(Integer, ForeignKey('contact.contact_id'))
    
    contact = relationship('Contact', uselist=False, back_populates='addresses')

    def __repr__(self):
        return (f'<Address(address_id={self.address_id}, '
                f'apartment_number={self.apartment_number}, '
                f'street_number={self.street_number},'
                f'street_name={self.street_name},'
                f'city={self.city},'
                f'province={self.province})>')

class EmailAddress(Base):
    __tablename__ =  'email_address'

    email_address_id = Column(Integer, primary_key=True)
    email_address = Column(String)
    
    contact_id = Column(Integer, ForeignKey('contact.contact_id'))

    contact = relationship('Contact', uselist=False, back_populates='email_addresses')

    def __repr__(self):
        return (f'<EmailAddress(email_address_id={self.email_address_id}, '
                f'email_address={self.email_address})>')

class PhoneNumber(Base):
    __tablename__ = 'phone_number'

    phone_number_id = Column(Integer, primary_key=True)
    phone_number = Column(String)
    
    phone_number_type_id = Column(Integer, ForeignKey('phone_number_type.phone_number_type_id'))

    contacts = relationship('Contact', 
                           secondary=contact_person_number_table)
    phone_number_type =  relationship('PhoneNumberType')

    def __repr__(self):
        return (f'<PhoneNumber(phone_number_id={self.phone_number_id}, '
                f'phone_number={self.phone_number})>')

class PhoneNumberType(Base):
    __tablename__ = 'phone_number_type'

    phone_number_type_id = Column(Integer, primary_key=True)
    phone_number_type = Column(String)

    def __repr__(self):
        return (f'<PhoneNumberType(phone_number_type_id={self.phone_number_type_id}, '
                f'phone_number_type={self.phone_number_type})>')


engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

# Create a new contact and associated data
contact1 = Contact(first_name='Russell', last_name='Yorke', date_of_birth=datetime(1983, 10, 23))
print(repr(contact1))

address1 = Address(street_number=191, street_name='Sherbrooke St', city='Winnipeg', province='Manitoba')
print(repr(address1))
print(repr(contact1.addresses))
contact1.addresses.append(address1)
print(repr(contact1.addresses))

email_addr1 = EmailAddress(email_address='r.y@gmail.com')
print(repr(email_addr1))
print(repr(contact1.email_addresses))
contact1.email_addresses.append(email_addr1)

phone_type = PhoneNumberType(phone_number_type='Cell')
phone_number1  = PhoneNumber(phone_number='4315551717', phone_number_type=phone_type)
print(repr(phone_type))
print(repr(phone_number1))
contact1.phone_numbers.append(phone_number1)

session.add(contact1)
for row in session.new:
    print(repr(row))

session.commit()

# Querying records
query_results = session.query(Contact, Address).filter_by(first_name='Russell').all()
print(repr(query_results))
contact, address = query_results[0]
print(repr(contact))
print(repr(address))

# Using models  to walk tables
contact = session.query(Contact).filter_by(first_name='Russell').first()
print(repr(contact))
print(repr(contact.addresses))
print(repr(contact.email_addresses))
print(repr(contact.phone_numbers))

# Using join syntax (left-outer-join) to find users who have a gmail
# address
query_results = session.query(Contact).join(EmailAddress).filter(EmailAddress.email_address.ilike('%gmail%'))
contacts = query_results.all()
for contact in contacts:
    print(repr(contact))
    for email in contact.email_addresses:
        print(repr(email))
    print()

# More efficient (less queries)
query_results = session.query(Contact, EmailAddress).join(EmailAddress).filter(EmailAddress.email_address.ilike('%gmail%'))
for contact, email_address in query_results:
    print(repr(contact))
    print(repr(email_address))
    print()