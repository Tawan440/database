from sqlalchemy import create_engine, Integer, String, inspect
from sqlalchemy.orm import DeclarativeBase, mapped_column, sessionmaker, Session, Mapped
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Body, status
# Define the base class for declarative models
class Base(DeclarativeBase):
    def as_dict(self):
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self.mapper.column_attrs)
        }

# Database manager class
class DataBaseManager:
    DATABASE = 'burger'
    URL = f'sqlite:///class_project.{DATABASE}'  # Ensure .db extension for SQLite
    engine = create_engine(URL)

    def get_session(self) -> sessionmaker:
        return sessionmaker(self.engine)

    def create_databases(self) -> None:
        Base.metadata.create_all(self.engine)  # Create tables based on Base metadata

DbManager = DataBaseManager()
DbManager.create_databases()  # Ensure this is called to create tables
NewSession = DbManager.get_session()

# Define the Burger model
class BurgerModel(Base):
    __tablename__ = 'burger'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    price: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String, unique=True)
    cheese: Mapped[int] = mapped_column(Integer)
    beef: Mapped[int] = mapped_column(Integer)

# Function to create or retrieve a burger
def repo_create_menu(burger_data: Dict[str, Any]) -> Dict[str, Any]:
    try:
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
            s.commit()
            return {
                "name": new_menu.name,
                "price": new_menu.price,
                "cheese": new_menu.cheese,
                "beef": new_menu.beef
            }
    except SQLAlchemyError as e:
        print(f"Database error in repo_create_menu: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")

# Function to retrieve a burger by ID
def repo_gimme_burger(id: int) -> Optional[Dict[str, Any]]:
    print(id)
    try:
        with NewSession() as s:
            existing_burger = s.get(BurgerModel, id)
            print(existing_burger)
            if existing_burger:
                return {
                    "name": existing_burger.name,
                    "price": existing_burger.price,
                    "cheese": existing_burger.cheese,
                    "beef": existing_burger.beef
                }
            return None
    except SQLAlchemyError as e:
        print(f"Database error in repo_gimme_burger: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")
