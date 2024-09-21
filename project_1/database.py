from sqlalchemy import create_engine, Integer, String, inspect, delete
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
    URL = f'sqlite:///class_project.{DATABASE}'
    engine = create_engine(URL)

    def get_session(self) -> sessionmaker:
        return sessionmaker(self.engine)

    def create_databases(self) -> None:
        Base.metadata.create_all(self.engine)  

DbManager = DataBaseManager()
DbManager.create_databases() 
NewSession = DbManager.get_session()

class BurgerModel(Base):
    __tablename__ = 'burger'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    price: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String, unique=True)
    cheese: Mapped[int] = mapped_column(Integer)
    beef: Mapped[int] = mapped_column(Integer)


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
from typing import Dict, Any, Optional
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

def dun_like_bruger(id: int) -> Optional[Dict[str, str]]:
    print(f"Attempting to delete burger with ID: {id}")
    try:
        with NewSession() as s:
            existing_burger = s.get(BurgerModel, id)
            if existing_burger:
                print(f"Found burger: {existing_burger}")
                s.delete(existing_burger)
                s.commit()  # Commit the transaction
                print("Burger deleted and changes committed.")
                return {
                    "message": "The burger has been thrown away..."
                }
            else:
                print("No burger found with the given ID.")
                return {
                    "message": "That not even exist"
                }
    except SQLAlchemyError as e:
        print(f"Database error in dun_like_bruger: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")
    
def change_burger(id: int, new_data: dict) -> Optional[Dict[str, str]]:
    try:
        with NewSession() as s:
            existing_burger = s.get(BurgerModel, id)
            if existing_burger:
                # Update fields
                for key, value in new_data.items():
                    if hasattr(existing_burger, key):
                        setattr(existing_burger, key, value)
                # Commit the transaction
                s.commit()
                return {"message": "Burger updated successfully"}
            else:
                return {"message": "Burger not found"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))