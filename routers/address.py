import sys
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import models
from schemas import NewAddress
from database import SessionLocal
from routers.auth import get_current_user, get_user_exception

sys.path.append("..")

router = APIRouter(
    prefix = "/address",
    tags = ["address"],
    responses={404:{"description":"Not found"}}
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@router.post("/")
async def create_address(address: NewAddress,
                        user: dict = Depends(get_current_user),
                        db :Session = Depends(get_db)):
    if not user:
        raise get_user_exception()
    address_model = models.Address()
    address_model.address1 = address.address1
    address_model.address2 = address.address2
    address_model.city = address.city
    address_model.state = address.state
    address_model.country = address.country
    address_model.postalcode = address.postalcode
    address_model.apt_num = address.apt_num

    db.add(address_model)
    db.flush()

    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()

    user_model.address_id = address_model.id

    db.add(user_model)

    db.commit()
