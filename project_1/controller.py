from fastapi import FastAPI, HTTPException, Body, Depends, status
from pydantic import BaseModel
from typing import Dict, Optional
from sqlalchemy.orm import Session
from database import repo_create_menu, repo_gimme_burger, dun_like_bruger, change_burger

app = FastAPI()

class BurgerPayload(BaseModel):
    price: int
    name: str
    cheese: int
    beef: int

@app.post('/burger/')
def create_burger(payload: BurgerPayload = Body(...)) -> dict:
    print(payload)
    try:
        # Convert the Pydantic model to a dictionary
        payload_dict = payload.dict()
        result = repo_create_menu(payload_dict)
        return result
    except HTTPException as e:
        # Handle HTTP exceptions
        raise e
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@app.get('/burger/{id}')
def get_burger(id: int) -> dict:
    print(id)
    try:
        result = repo_gimme_burger(id)
        if result:
            return result
        else:
            return {'error': 'No burger found with this ID'}
    except HTTPException as e:
        # Handle HTTP exceptions
        raise e
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@app.delete('/burger/{id}')
def get_burger(id: int) -> dict:
    print(id)
    try:
        result = dun_like_bruger(id)
        if result:
            return result
        else:
            return {'error': 'No burger found with this ID'}
    except HTTPException as e:
        # Handle HTTP exceptions
        raise e
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@app.put('/burger/{id}')
def get_burger(id: int) -> dict:
    print(id)
    try:
        result = change_burger(id)
        if result:
            return result
        else:
            return {'error': 'No burger found with this ID'}
    except HTTPException as e:
        # Handle HTTP exceptions
        raise e
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
