from unqlite import UnQLite
from flask import g

DATABASE = 'app.db'

def get_db():
    db = getattr(g, '__database', None)
    if db is None:
        db = g.__database = UnQLite(DATABASE)
    return db

#@app.teardown_appcontext
def close_connection():
    db = getattr(g, '__database', None)
    if db is not None:
        db.close()
