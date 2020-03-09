from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from interface.controller.purchase_controller import PurchaseController
from interface.exceptions.not_sufficient_points import NotSufficientPoints
from interface.utils import oauth2_scheme, get_current_user, get_db
from models import User, Generator

router = APIRouter()


@router.get('/available')
async def available_generators(token: str = Depends(oauth2_scheme)):
    return {'message': 'token'}


@router.post('/{generator_id}/buy')
async def buy_generator(generator_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    generator = db.query(Generator).filter(Generator.id == generator_id).first()
    if generator is None:
        return HTTPException(
            status_code=404,
            detail=f'Generator {generator_id} does not exists',
        )
    try:
        user_generator_purchase = PurchaseController(db).buy_generator(user, generator)
    except NotSufficientPoints as exception:
        raise HTTPException(
            status_code=400,
            detail=str(exception),
        )
    return user_generator_purchase.__dict__
