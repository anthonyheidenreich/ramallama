import os
from paver.easy import task, sh, needs
from paver.virtual import virtualenv

venv = os.environ['VENV']


@task
@virtualenv(dir=venv)
def makemigrations():
    sh('python ramallama/manage.py makemigrations')


@task
@virtualenv(dir=venv)
def migrate():
    sh('python ramallama/manage.py migrate')


@task
@virtualenv(dir=venv)
def run():
    sh('python ramallama/manage.py runserver 8000')


@task
@virtualenv(dir=venv)
@needs('lint')
def test():
    """Run flake8 and any tests
    """
    pass


@task
@virtualenv(dir=venv)
def lint():
    """Run flake8 and any tests
    """
    sh('flake8 . --exclude migrations')
