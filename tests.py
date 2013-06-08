# tests for the main app
import unittest
from app import lido_app, db
from app.models import User, TemperatureRecord
from flask.ext.sqlalchemy import sqlalchemy


class BaseModelTestCase(unittest.TestCase):
    "Define base model setUp and tearDown methods."

    def setUp(self):
        lido_app.config['TESTING'] = True
        lido_app.config['CSRF_ENABLED'] = False
        lido_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = lido_app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # def _create_test_user(self, save=True):
    #     "Helper method to create a new user (and optionally save model)."
    #     pass


class UserModelTestCase(BaseModelTestCase):

    def test_create_user(self):
        u = User(username="fred")
        u.save()
        self.assertIsNotNone(u.id)
        self.assertEqual(u.username, 'fred')
        self.assertEqual(u.get_id(), u'fred')
        self.assertIsNone(u.oauth_token)
        self.assertIsNone(u.oauth_token_secret)

    def test_create_user_2(self):
        u = User(username="fred", token='token', secret='secret')
        u.save()
        self.assertEqual(u.oauth_token, 'token')
        self.assertEqual(u.oauth_token_secret, 'secret')

    def test_duplicate_user(self):
        "Test that saving a duplicate user performs an upsert."
        u = User(username='fred', token='token', secret='secret')
        u.save()
        u2 = User(username='fred')
        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            u2.save()
        db.session.rollback()
        self.assertIsNone(u2.id)


class TemperatureModelTestCase(BaseModelTestCase):

    def test_create_temperature(self):
        "Create a new temperature record for a given user."
        u = User(username="fred", token='token', secret='secret')
        u.save()
        t = TemperatureRecord(user=u, location="brockwell", temperature=16.2)
        t.save()
        self.assertIsNotNone(t.id)
        self.assertEqual(t.submitted_by, u)
        self.assertEqual(t.location, 'brockwell')
        self.assertEqual(t.temperature, 16.2)
        self.assertEqual(len(u.recordings), 1)
        self.assertEqual(u.recordings[0], t)

if __name__ == '__main__':
    unittest.main()
