from typing import Annotated
from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db
import models
import schemas

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]


@app.get('/', status_code=status.HTTP_200_OK)
async def all_todos(db: db_dependency):
    data = db.query(models.Todo).all()
    return data


@app.get('/{id}', status_code=status.HTTP_200_OK)
async def get_todo(id: int, db: db_dependency):
    data = db.query(models.Todo).filter(models.Todo.id == id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')
    return data


@app.post('/create', status_code=status.HTTP_201_CREATED)
async def create_todo(request: schemas.TodoRequest, db: db_dependency):
    todo_model = models.Todo(**request.dict())
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


@app.put('/update/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(id: int, request: schemas.TodoRequest, db: db_dependency):
    data = db.query(models.Todo).filter(models.Todo.id == id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')
    data.title = request.title
    data.description = request.description
    data.priority = request.priority
    data.complete = request.complete
    db.add(data)
    db.commit()
    db.refresh(data)
    return {'detail': 'Todo updated successfully'}
