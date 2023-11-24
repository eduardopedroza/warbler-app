"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_user_repr(self):
        """Does the repr method work as expected?"""
        self.assertEqual(repr(self.user1), f"<User #{self.user1.id}: {self.user1.username}, {self.user1.email}>")

    def test_is_following(self):
        """Does is_following successfully detect when user1 is following user2?"""
        self.user1.following.append(self.user2)
        db.session.commit()
        self.assertTrue(self.user1.is_following(self.user2))

    def test_is_not_following(self):
        """Does is_following successfully detect when user1 is not following user2?"""
        self.assertFalse(self.user1.is_following(self.user2))

    def test_is_followed_by(self):
        """Does is_followed_by successfully detect when user1 is followed by user2?"""
        self.user2.following.append(self.user1)
        db.session.commit()
        self.assertTrue(self.user1.is_followed_by(self.user2))

    def test_is_not_followed_by(self):
        """Does is_followed_by successfully detect when user1 is not followed by user2?"""
        self.assertFalse(self.user1.is_followed_by(self.user2))

    def test_user_signup(self):
        """Does User.create successfully create a new user given valid credentials?"""
        user = User.signup("testuser3", "test3@test.com", "password", None)
        db.session.commit()
        self.assertIsNotNone(User.query.filter_by(username="testuser3").first())

    def test_user_signup_fail(self):
        """Does User.create fail to create a new user if any of the validations fail?"""
        with self.assertRaises(Exception):
            User.signup("user1", "test4@test.com", "password", None)
            db.session.commit()

    def test_user_authenticate_success(self):
        """Does User.authenticate successfully return a user when given a valid username and password?"""
        user = User.authenticate(self.user1.username, "password")
        self.assertIsNotNone(user)

    def test_user_authenticate_invalid_username(self):
        """Does User.authenticate fail to return a user when the username is invalid?"""
        self.assertFalse(User.authenticate("wrongusername", "password"))

    def test_user_authenticate_invalid_password(self):
        """Does User.authenticate fail to return a user when the password is invalid?"""
        self.assertFalse(User.authenticate(self.user1.username, "wrongpassword"))