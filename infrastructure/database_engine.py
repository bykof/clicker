from sqlalchemy import create_engine

from constants import POSTGRES_URL

engine = create_engine(POSTGRES_URL, pool_size=100, max_overflow=-1)
