from sqlalchemy.orm import DeclarativeBase, mapped_column, sessionmaker, Session, Mapped
from sqlalchemy import create_engine, Integer, String, select, inspect
from typing import Dict, Any, Optional

class Base(DeclarativeBase):
    def as_dict(self):
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self.mapper.column_attrs)
        }

class DataBaseManager:
    DATABASE = 'burger'
    URL = f'sqlite:///class_project.{DATABASE}'
    engine = create_engine(URL)

    def get_session(self) -> sessionmaker[Session]:
        return sessionmaker(self.engine)

    def create_databases(self) -> None:
        Base.metadata.create_all(self.engine)

DbManager = DataBaseManager()
DbManager.create_databases()
NewSession = DbManager.get_session()

class BurgerModel(Base):
    __tablename__ = 'burger'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Added primary key column
    price: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String, unique=True)  # Added unique constraint to name
    cheese: Mapped[int] = mapped_column(Integer)
    beef: Mapped[int] = mapped_column(Integer)
DbManager.create_databases()
def repo_create_menu(burger_data: Dict[str, Any]) -> Dict[str, Any]:
    with NewSession() as s:
        stmt = select(BurgerModel).where(BurgerModel.name == burger_data['name'])
        existing_burger = s.execute(stmt).scalar_one_or_none()
        if existing_burger:
            return {
                "name": existing_burger.name,
                "price": existing_burger.price,
                "cheese": existing_burger.cheese,
                "beef": existing_burger.beef
            }
        new_menu = BurgerModel(**burger_data)
        s.add(new_menu)
        s.commit()  # Commit the transaction inside the 'with' block
    
        return {
            "name": new_menu.name,
            "price": new_menu.price,
            "cheese": new_menu.cheese,
            "beef": new_menu.beef
        }

def repo_gimme_burger(burger_name: str) -> Optional[dict]:
    with NewSession as s:
        stmt = select(BurgerModel).where(BurgerModel.name == burger_name)
        existing_burhger = s.execute(stmt).scalar_one_or_none()
        if existing_burhger:
             return {
            "name": existing_burhger.name,
            "price": existing_burhger.price,
            "cheese": existing_burhger.cheese,
            "beef": existing_burhger.beef
            }