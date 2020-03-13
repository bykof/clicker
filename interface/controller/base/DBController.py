from sqlalchemy.orm import Session


class DBController:
    def __init__(self, db: Session):
        self.db = db
