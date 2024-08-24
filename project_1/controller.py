from fastapi import Body, FastAPI, HTTPException, status, Request
from pydantic import BaseModel
from database import repo_create_menu, repo_gimme_burger

app = FastAPI()

class BurgerPayload(BaseModel):
    price: int
    name: str
    cheese: int
    beef: int

@app.post('/burger/')
def create_burger(payload: BurgerPayload = Body(...)) -> dict:
    try:
        # Convert the Pydantic model to a dictionary
        payload_dict = payload.dict()
        result = repo_create_menu(payload_dict)
        return result
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@app.get('/burger/{id}')
def get_burger_name(request: Request, name: str) -> dict:
    burger = repo_gimme_burger(name)
    if burger:
        return burger
    return{'error': 'no burger'}