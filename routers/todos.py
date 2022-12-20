import sys
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from routers.auth import get_current_user, get_user_exception
import models
from schemas import Todo
from database import SessionLocal, engine

sys.path.append("..")

router = APIRouter(prefix="/todos",
                    tags=["todos"],
                    responses={404:{"user":"Not found"}}
                    )

models.Base.metadata.create_all(bind = engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def succesful_response(status_code: int):
    return {'status':{status_code},
            'transaction':'Succesful'}

def http_exception_not_found():
    return HTTPException(status_code = 404, detail = 'Todo not found')

@router.get('/')
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()

@router.get('/{todo_id}')
async def read_todo(todo_id: int,
                    user: dict = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    if not user:
        raise get_user_exception

    todo_model = db.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .filter(models.Todos.owner_id == user.get("id"))\
        .first()

    if todo_model:
        return todo_model
    raise http_exception_not_found()

@router.get('/user')
async def read_all_by_user(user: dict = Depends(get_current_user),
                            db: Session = Depends(get_db)):
    if not user:
        raise get_user_exception
    return db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all()

@router.post('/')
async def create_todo(todo: Todo,
                        user: dict = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    if not user:
        raise get_user_exception

    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.owner_id = user.get("id")

    db.add(todo_model)
    db.commit()

    return succesful_response(201)

@router.put('/{todo_id}')
async def update_todo(todo_id: int,
                    todo: Todo, db: Session = Depends(get_db),
                    user: dict = Depends(get_current_user)):
    if not user:
        raise get_user_exception
    todo_model = db.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .filter(models.Todos.owner_id == user.get("id"))\
        .first()
    if not todo_model:
        raise http_exception_not_found()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()

    return succesful_response(200)

@router.put('/complete/{todo_id}')
async def complete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if not todo_model:
        raise http_exception_not_found()
    todo_model.complete = True

    db.add(todo_model)
    db.commit()

    return succesful_response(200)

@router.delete('/{todo_id}')
async def delete_todo(todo_id: int,
                        user: dict = Depends(get_current_user),
                        db: Session = Depends(get_db)):

    if not user:
        raise get_user_exception

    todo_model = db.query(models.Todos)\
    .filter(models.Todos.id == todo_id)\
    .filter(models.Todos.owner_id == user.get("id"))\
    .first()
    if not todo_model:
        raise http_exception_not_found()

    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()

    return succesful_response(200)
