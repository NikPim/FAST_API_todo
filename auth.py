from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
import models
from schemas import NewUser

SECREY_KEY = "Penek"
ALGORITHM = "HS256"
bcrypt_context= CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()
models.Base.metadata.create_all(bind = engine)
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

def get_password_hash(password):

    return bcrypt_context.hash(password)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def verify_password(input_password, hash_password):

    return bcrypt_context.verify(input_password, hash_password)

def authenticate_user(username: str, password: str, db):
    user = db.query(models.Users).filter(models.Users.username == username).first()

    if not user or not verify_password(password, user.hashed_password):
        return False

    return user

def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    encode = {"sub": username, "id": user_id, "exp": expire}

    return jwt.encode(encode, SECREY_KEY, algorithm = ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECREY_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if not username or not user_id:
            raise get_user_exception()
        return {"username": username, "id": user_id}
    except:
         raise get_user_exception()


@app.post('/create/user')
async def create_user(new_user: NewUser, db: Session = Depends(get_db)):
    new_user_model = models.Users()
    new_user_model.email = new_user.email
    new_user_model.first_name = new_user.first_name
    new_user_model.last_name = new_user.last_name
    new_user_model.hashed_password = get_password_hash(new_user.password)
    new_user_model.username = new_user.username
    new_user_model.is_active = True

    db.add(new_user_model)
    db.commit()

    return {'status':'201',
            'transaction':'Succesful'}

@app.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()

    token_expires = timedelta(minutes = 20)
    token = create_access_token(user.username, user.id, expires_delta=token_expires)

    return {"token": token}


#Exceptions
def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could't validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    return credentials_exception

def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )

    return token_exception_response
