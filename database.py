from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models
    import models.recipe
    Base.metadata.create_all(bind=engine)


#from unqlite import UnQLite
#from flask import g
#
#DATABASE = 'app.db'
#
#def get_db():
#    db = getattr(g, '__database', None)
#    if db is None:
#        db = g.__database = UnQLite(DATABASE)
#    return db
#
##@app.teardown_appcontext
#def close_connection():
#    db = getattr(g, '__database', None)
#    if db is not None:
#        db.close()
