#!flask/bin/python
import os
import unittest
from app import app, db
from app.models import User

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root_maria@localhost/db_todo_tests'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_createUser(self):
        u = User(nickname='john', email='john@example.com', pwd = '123', active = True)
        db.session.add(u)
        db.session.commit()
        user = User.query.filter(User.nickname=='john')
        assert user != None
        print 'Create User OK'

    def test_login_user(self):
        u = User(nickname='john', email='john@example.com', pwd = '123', active = True)
        db.session.add(u)
        db.session.commit()
        user = User.query.filter(
                                User.nickname == 'john',
                                ((User.active.is_(None))|(User.active != False)),
                                ).first()
        assert True == user.verify_password('123')
        print 'login user OK'

if __name__ == '__main__':
    unittest.main()
