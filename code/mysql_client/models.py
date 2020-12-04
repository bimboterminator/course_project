from sqlalchemy import Column, Integer, String, Date, ForeignKey,SmallInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(Base):
    # В __tablename__ указывается имя таблицы, которую мы хотим создать
    __tablename__ = 'test_users'
    # __table_args__ используется для установки кодировки в базе на utf8, т. к. мы записываем в нее кириллицу.
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(16), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    access = Column(SmallInteger, nullable=True, default=0)
    active = Column(SmallInteger, nullable=True, default=0)
    start_active_time = Column(Date, nullable=True)

    # Метод __repr__ используется для того, чтобы можно было сделать красивый вывод полей нашей модели
    # при обращении к ней из дебага или просто печати ее содердимого.
    # Сравните вывод print(PrepodInstance):
    # без __repr__ : <models.models.Prepod object at 0x7fe25dc9eac0>
    # с __repr__   : <Prepod(id='2',name='Clarence', surname='Wright', start_teaching='2002-11-30')>
    def __repr__(self):
        return f"<USERS(" \
               f"id='{self.id}'," \
               f"username='{self.username}', " \
               f"email='{self.email}', " \
               f"access='{self.access}'" \
               f"active='{self.active}'"\
               f"start_active_time='{self.start_active_time}'"\
               f")>"
