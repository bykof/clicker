from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from interface.controller.available_generators_controller import AvailableGeneratorsController
from interface.controller.purchase_controller import PurchaseController
from interface.exceptions.not_sufficient_points import NotSufficientPoints
from interface.models.generators import GeneratorPurchase as GeneratorPurchaseModel, Generator as GeneratorModel
from interface.utils import get_current_user, get_db
from models import User, Generator

router = APIRouter()


@router.get('/available', response_model=List[GeneratorModel])
async def available_generators(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return AvailableGeneratorsController(db).available_generators(user)


@router.get('/current-user', response_model=List[GeneratorPurchaseModel])
async def get_current_users_generators(user: User = Depends(get_current_user)):
    return user.generator_purchases


@router.post('/{generator_id}/buy', response_model=GeneratorPurchaseModel)
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
    return user_generator_purchase
