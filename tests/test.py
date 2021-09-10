import json
from api import db
from app import app
from unittest import TestCase
from api.models.user import UserModel
from base64 import b64encode


class TestUsers(TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_user_creation(self):
        user_data = {
            "username": 'admin',
            'password': 'admin',
            'role': 'admin'
        }
        res = self.client.post('/users', data=user_data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertIn('admin', data.values())

    def test_users_get(self):
        users_data = [
            {
                "username": 'admin',
                'password': 'admin',
                'role': 'admin'
            },
            {
                "username": 'ivan',
                'password': '12345',
                'role': 'simple_user'
            },
        ]
        for user_data in users_data:
            user = UserModel(**user_data)
            user.save()

        res = self.client.get('/users')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        # print(data)
        self.assertEqual(data[0]["username"], users_data[0]["username"])
        self.assertEqual(data[1]["username"], users_data[1]["username"])
        self.assertEqual(data[0]["role"], users_data[0]["role"])

    def test_user_not_found(self):
        res = self.client.get('/users/1')
        self.assertEqual(res.status_code, 404)

    def test_author_creation(self):
        authors_data = {
            "name": 'Alex',
            "surname": "Petroff"
        }
        self.create_and_auth_user()
        res = self.client.post('/authors', headers=self.headers, data=authors_data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Alex', data.values())
        self.assertIn('Petroff', data.values())

    def create_and_auth_user(self):
        user_data = {
            "username": 'admin',
            'password': 'admin',
            'role': 'admin'
        }

        user = UserModel(**user_data)
        user.save()
        self.user = user
        # "login:password" --> b64 --> 'ksjadhsadfh474=+d'
        self.headers = {
            'Authorization': 'Basic ' + b64encode(
                f"{user_data['username']}:{user_data['password']}".encode('ascii')).decode('utf-8')
        }

    def test_author_creation_neg(self):
        authors_data = {
            "name": 'Alex',
            "surname": "Petroff"
        }
        self.create_and_auth_user_neg()
        res = self.client.post('/authors', headers=self.headers, data=authors_data)
        self.assertEqual(res.status_code, 403)

    def create_and_auth_user_neg(self):
        user_data = {
            "username": 'admin',
            'password': 'admin',
            'role': 'not admin'
        }

        user = UserModel(**user_data)
        user.save()
        self.user = user
        # "login:password" --> b64 --> 'ksjadhsadfh474=+d'
        self.headers = {
            'Authorization': 'Basic ' + b64encode(
                f"{user_data['username']}:{user_data['password']}".encode('ascii')).decode('utf-8')
        }

    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
