from fabric.api import task, run
from unqlite import UnQLite

from database import DATABASE

@task
def create_db():
    db = UnQLite(DATABASE)

    # TODO: do for all collections, if there are multiple
    recipes = db.collection('recipes')

    if not recipes.exists():
        with db.transaction():
            recipes.create()
