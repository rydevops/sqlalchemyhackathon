from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class NetworkDevice(Base):
    __tablename__ = 'networkdevice'

    device_id = Column(Integer, primary_key=True, autoincrement=True)
    device_name = Column(String(50), nullable=False)
    vendor_id = Column(Integer, ForeignKey('networkdevicevendor.vendor_id'))

    vendor = relationship('NetworkDeviceVendor', back_populates='network_device')

class NetworkDeviceVendor(Base):
    __tablename__ = 'networkdevicevendor'

    vendor_id = Column(Integer, primary_key=True, autoincrement=True)
    vendor_name = Column(String(50), nullable=False)

    network_device = relationship('NetworkDevice', uselist=False)

    def has_network_device(self):
        return self.network_device is not None

Base.metadata.create_all(engine)

ndv = NetworkDeviceVendor(vendor_name='Cisco')
ndv2 = NetworkDeviceVendor(vendor_name='Juniper')
nd = NetworkDevice(device_name='demo1', vendor=ndv)
session.add(ndv)
session.add(ndv2)
session.add(nd)
session.commit()

