from interface.services.game_service import GameService
from models import User


class GameController:

    def __init__(self,  user: User, game_service: GameService):
        self.user = user
        self.game_service = game_service

    def click(self):
        self.game_service.add_click_to_balance()