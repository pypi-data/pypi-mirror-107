from typing import Optional, Any
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from services_reviews.common_utils.read_conf import ReadConf

class dbConnector:
    engine : Optional[Engine]  = None
    session : Optional[Session] = None

    @classmethod
    def start_connect_db(cls):
        cls.init_db()
        cls.create_session()

    @classmethod
    def init_db(cls):
        DB_USER = ReadConf.get("db", "db", 'user')
        DB_PASSWORD = ReadConf.get("db", "db", 'password')
        DB_HOST = ReadConf.get("db", "db", "HOST")
        DB_PORT = ReadConf.get("db", "db", "PORT")
        DB_DATABASE = ReadConf.get("db", "db", "database")
        database_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
        cls.engine = create_engine(database_url)

    @classmethod
    def create_session(cls):
        # Создаем фабрику для создания экземпляров Session. Для создания фабрики в аргументе
        # bind передаем объект engine
        FactorySession = sessionmaker(bind=cls.engine)
        # Создаем объект сессии из вышесозданной фабрики Session
        cls.session = FactorySession()

    @classmethod
    def disconnect(cls):
        cls.session.close()
        cls.engine.dispose()
