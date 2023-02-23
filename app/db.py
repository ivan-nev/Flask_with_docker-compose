import atexit
import config
from sqlalchemy import Column, String, Integer, DateTime, create_engine, func, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from config import PG_DSN




# PG_DSN = 'postgresql://app:123@0.0.0.0:5432/netology'
PG_DNS = config.PG_DSN
engine = create_engine(PG_DSN)

Base = declarative_base()
Session = sessionmaker(bind=engine)
#закрытие сесии после завершения программы
atexit.register(engine.dispose)

# создаём таблицы
class User(Base):

    __tablename__ = 'app_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    advertisements = relationship('Advertisement', backref='user', cascade="all, delete")



class Advertisement(Base):

    __tablename__ = 'advertisements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    id_user = Column(Integer, ForeignKey('app_user.id', ondelete='CASCADE'))
    # user = relationship('User', lazy="joined", backref='advertisements')


Base.metadata.create_all(bind=engine)