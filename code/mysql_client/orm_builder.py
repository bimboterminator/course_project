from faker import Faker
from random import randint
import time
from sqlalchemy.orm import sessionmaker
from mysql_client.models import Base, Users
from mysql_client.mysql_orm_client import MysqlOrmConnection

fake = Faker()


class MysqlOrmBuilder(object):
    def __init__(self, connection: MysqlOrmConnection):
        self.connection = connection
        self.engine = self.connection.connection.engine

    def add_user(self, access=True):
        if access:
            right = 1
        else:
            right = 0
        user = Users(
            username=fake.last_name()+f'{randint(1000,6000)}',
            password=fake.password(length=40, special_chars=False, upper_case=False),
            email=fake.email(),
            access=right
        )
        self.connection.session.add(user)
        self.connection.session.commit()
        return user

    def delete_user(self, ident):
        res = self.connection.session.query(Users).filter_by(id=ident)
        res.delete()
        self.connection.session.commit()

    def user_is_present(self, email):
        session = sessionmaker(bind=self.connection.get_connection())
        self.connection.session = session()
        usr = self.connection.session.query(Users).filter_by(email=email).first()
        self.connection.connection.close()
        if usr:
            return True
        else:
            return False

    def get_user(self, email):
        session = sessionmaker(bind=self.connection.get_connection())
        self.connection.session = session()
        usr = self.connection.session.query(Users).filter_by(email=email).first()
        self.connection.connection.close()
        return usr

    def get_granted_user(self):
        return self.connection.session.query(Users).filter_by(access=1).first()

"""   self.create_prepods()
       self.create_students()

   def create_prepods(self):
       if not self.engine.dialect.has_table(self.engine, 'prepods'):
           Base.metadata.tables['prepods'].create(self.engine)

   def create_students(self):
       if not self.engine.dialect.has_table(self.engine, 'students'):
           Base.metadata.tables['students'].create(self.engine)
"""