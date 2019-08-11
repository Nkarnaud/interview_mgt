from flask_testing import TestCase
from project import create_app, db


# App initialisation
app = create_app()


# Defining the base test configuration
class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app

    # Database setup
    def setUp(self):
        db.create_all()
        db.session.commit()

    # Database tear down
    def tearDown(self):
        db.session.remove()
        db.drop_all()
