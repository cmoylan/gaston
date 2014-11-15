from fabric.api import task, run
from gaston.database import init_db


@task
def create_db():
    init_db()
