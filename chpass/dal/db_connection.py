from typing import Type, Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

from chpass.dal.models.base import Base
from chpass.dal.session import session_scope


class DBConnection(object):
    def __init__(self) -> None:
        self._connection = None
        self._session_class = None

    def connect(self, protocol: str, database: str) -> None:
        url = URL.create(protocol, database=str(database))
        engine = create_engine(url)
        self._session_class = sessionmaker(bind=engine)
        self._connection = engine.connect()

    def select(self, model: Type[Base], filters: tuple = (), serializable: bool = False) -> list:
        with session_scope(self._session_class) as session:
            query = session.query(model).filter(*filters)
            results = query.all()
            return [result.json() for result in results] if serializable else results

    def insert(self, row: Base) -> None:
        with session_scope(self._session_class) as session:
            session.add(row)

    def update(self, model: Type[Base], filters: tuple, column: Any, new_value: Any) -> None:
        with session_scope(self._session_class) as session:
            row = session.query(model).filter(*filters).one()
            setattr(row, column, new_value)

    def delete(self, model: Type[Base], filters: tuple) -> None:
        with session_scope(self._session_class) as session:
            row = session.query(model).filter(*filters).one()
            session.delete(row)

    def close(self) -> None:
        self._connection.close()
