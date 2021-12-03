from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum, Float, ForeignKey

Base = declarative_base()

#role = Enum['user', 'worker', 'admin']

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String)
    login = Column(String)
    password = Column(String)
    role = Column(String)

    def __repr__(self):
        return "<User(name='{}')>" \
            .format(self.name)


class Medicament(Base):
    __tablename__ = 'medicament'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String)
    price = Column(Float)
    number = Column(Integer)

    def __repr__(self):
        return "<Product(name='{}', price='{}', number={})>" \
            .format(self.name, self.price, self.number)


class Purchase(Base):
    __tablename__ = 'purchase'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    product_id = Column(Integer, ForeignKey('medicament.id'))
    number = Column(Integer)
    status = Column(String)

    def __repr__(self):
        return "<Order(user='{}', product='{}', number={}, status='{}')>" \
            .format(self.user_id, self.product_id, self.number, self.status)

