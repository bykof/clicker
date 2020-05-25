from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from interface.controller.available_upgrades_controller import AvailableUpgradesController
from interface.controller.purchase_controller import PurchaseController
from interface.exceptions.not_sufficient_points import NotSufficientPoints
from interface.exceptions.upgrade_already_bought_error import UpgradeAlreadyBoughtError
from interface.models.upgrades import Upgrade as UpgradeModel, UpgradePurchase as UpgradePurchaseModel
from interface.utils import get_current_user, get_db
from models import User, Upgrade

router = APIRouter()


async def get_upgrade(upgrade_id: int, db: Session = Depends(get_db)) -> Upgrade:
    upgrade = db.query(Upgrade).filter(Upgrade.id == upgrade_id).first()
    if upgrade is None:
        raise HTTPException(
            status_code=404,
            detail=f'Upgrade {upgrade_id} does not exists',
        )
    return upgrade


@router.get('/available', response_model=List[UpgradeModel])
async def available_upgrades_for_current_user(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return AvailableUpgradesController(db).available_upgrades(user)


@router.get('/current-user', response_model=List[UpgradePurchaseModel])
async def get_upgrades_of_current_user(user: User = Depends(get_current_user)):
    return user.upgrade_purchases


@router.get('/{upgrade_id}/buy', response_model=UpgradePurchaseModel)
async def buy_upgrade_for_current_user(
    upgrade: Upgrade = Depends(get_upgrade),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        user_upgrade_purchase = PurchaseController(db).buy_upgrade(user, upgrade)
    except NotSufficientPoints as exception:
        raise HTTPException(
            status_code=400,
            detail=str(exception),
        )
    except UpgradeAlreadyBoughtError as exception:
        raise HTTPException(
            status_code=400,
            detail=str(exception),
        )
    return user_upgrade_purchase
