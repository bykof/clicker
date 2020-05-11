import os

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload

from infrastructure.redis_balance_client import RedisBalanceClient
from interface.utils import get_db
from models import User, GeneratorPurchase, UpgradePurchase, Generator, Upgrade

router = APIRouter()

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'))


@router.get('/')
async def dashboard(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).options(joinedload('generator_purchases'), joinedload('upgrade_purchases')).all()
    generator_purchases = db.query(GeneratorPurchase).all()
    upgrade_purchases = db.query(UpgradePurchase).all()
    generators = db.query(Generator).all()
    upgrades = db.query(Upgrade).all()
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "users": users,
            "generator_purchases": generator_purchases,
            "upgrade_purchases": upgrade_purchases,
            "generators": generators,
            "upgrades": upgrades,
            "clicks": {
                user.id: RedisBalanceClient(user).get_points()
                for user in users
            }
        },
    )
