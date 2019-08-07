# -*- coding: utf-8 -*-
from flask.cli import FlaskGroup
import datetime
from sqlalchemy import event
from project import db, create_app
from project.models.models import Interview, Interviewer, Candidates

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

''' @cli.command()
def seed_db():
    """Seeds the database."""
    db.session.add(favorite(
        firstname = 'Tsombeng',
        lastname = 'Arnaud',
        email = 'arnaud.tsombeng@gmail.com',
        password='password',
        dateofbirth = '02/09/1990',
        gender='M',
        tell='1254863458'
        ))
    db.session.add(favorite(
        firstname='justatest',
        lastname= 'testing',
        dateofbirth= '02/09/1986',
        email = 'tests@tests.com',
        password='password',
        gender='M',
        tell ='00688283',
    ))
    db.session.commit() '''

if __name__ == '__main__':
    cli()