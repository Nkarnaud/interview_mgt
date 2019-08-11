import os
import unittest
from flask import current_app
from flask_testing import TestCase
from project import create_app


app = create_app()
# App initialization


class TestDevelopmentConfig(TestCase):
    # Testing different configuration variable in dev environment

    def create_app(self):
        app.config.from_object('project.config.DevelopmentConfig')
        return app

    # Test dev enviroment
    def test_app_is_development(self):
        self.assertTrue(app.config['SECRET_KEY'] ==
                        os.environ.get('SECRET_KEY'))
        self.assertFalse(current_app is None)
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] ==
                        os.environ.get('DATABASE_URL'))
        self.assertTrue(app.config['DEBUG_TB_ENABLED'])
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])


# Testing different configuration variable in test environment
class TestTestingConfig(TestCase):

    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app

    # Test test enviroment
    def test_app_is_testing(self):
        self.assertTrue(app.config['SECRET_KEY'] ==
                        os.environ.get('SECRET_KEY'))
        self.assertTrue(app.config['TESTING'])
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] ==
                        os.environ.get('DATABASE_TEST_URL'))
        self.assertFalse(app.config['DEBUG_TB_ENABLED'])
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])


# Testing different configuration variable in prod environment
class TestProductionConfig(TestCase):

    def create_app(self):
        app.config.from_object('project.config.ProductionConfig')
        return app

    # Test prod enviroment
    def test_app_is_production(self):
        self.assertTrue(app.config['SECRET_KEY'] ==
                        os.environ.get('SECRET_KEY'))
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] ==
                        os.environ.get('DATABASE_URL'))
        self.assertFalse(app.config['TESTING'])
        self.assertFalse(app.config['DEBUG_TB_ENABLED'])


if __name__ == '__main__':
    unittest.main()
