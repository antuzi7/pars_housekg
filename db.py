from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Text,
    Integer,
    select,
)

from config import MYSQL_URL

engine = create_engine(MYSQL_URL)
meta = MetaData()


class HouseManager():

    def __init__(self, engine) -> None:
        self.engine = engine
        self.house = self.get_table_schema()

    def get_table_schema(self):
        house = Table(
            "house", meta,
            Column("id", Integer, primary_key=True),
            Column("title", String(200)),
            Column("som", String(100)),
            Column("dollar", String(100)),
            Column("mobile", String(50)),
        )
        return house

    def create_table(self):
        meta.create_all(self.engine, checkfirst=True)
        print("Таблица успешно создано")

    def insert_house(self, data):
        ins = self.house.insert().values(
            **data
        )
        connect = self.engine.connect()
        result = connect.execute(ins)
        connect.commit()