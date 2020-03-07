from sqlalchemy import create_engine

engine = create_engine('postgres://localhost/clicker', echo=True)
