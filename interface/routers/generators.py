from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from application.game.generator_costs_calculator import GeneratorCostsCalculator
from interface.controller.available_generators_controller import AvailableGeneratorsController
from interface.controller.purchase_controller import PurchaseController
from interface.exceptions.not_sufficient_points import NotSufficientPoints
from interface.models.generators import GeneratorPurchase as GeneratorPurchaseModel, Generator as GeneratorModel
from interface.utils import get_current_user, get_db
from models import User, Generator, GeneratorPurchase

router = APIRouter()


async def get_generator(generator_id: int, db: Session = Depends(get_db)) -> Generator:
    generator = db.query(Generator).filter(Generator.id == generator_id).first()
    if generator is None:
        raise HTTPException(
            status_code=404,
            detail=f'Generator {generator_id} does not exists',
        )
    return generator


@router.get('/available', response_model=List[GeneratorModel])
async def available_generators_for_current_user(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return AvailableGeneratorsController(db).available_generators(user)


@router.get('/current-user', response_model=List[GeneratorPurchaseModel])
async def get_generators_of_current_user(user: User = Depends(get_current_user)):
    return user.generator_purchases


@router.get('/{generator_id}/next-price', response_model=float)
async def next_generator_price_for_current_user(
    generator: Generator = Depends(get_generator),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_generator_purchase = db.query(GeneratorPurchase).filter(
        GeneratorPurchase.user_id == user.id,
        GeneratorPurchase.generator_id == generator.id
    ).first()
    amount = 0
    if user_generator_purchase:
        amount = user_generator_purchase.amount

    return GeneratorCostsCalculator.calculate(
        generator,
        amount,
    )


@router.get('/{generator_id}/buy', response_model=GeneratorPurchaseModel)
async def buy_generator_for_current_user(
    generator: Generator = Depends(get_generator),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        user_generator_purchase = PurchaseController(db).buy_generator(user, generator)
    except NotSufficientPoints as exception:
        raise HTTPException(
            status_code=400,
            detail=str(exception),
        )
    return user_generator_purchase
