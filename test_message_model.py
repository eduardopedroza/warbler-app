from unittest import TestCase
from app import app
from models import db, User, Message

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///warbler_test'

class MessageModelTestCase(TestCase):
    """Tests for model for Messages."""

    @classmethod
    def setUpClass(cls):
        """Create test client and add sample data."""
        cls.client = app.test_client()

        db.create_all()
        User.query.delete()
        Message.query.delete()

        user = User.signup(username="testuser", email="test@test.com", password="password", image_url=None)
        db.session.commit()

        cls.user = User.query.filter_by(username="testuser").first()

    @classmethod
    def tearDownClass(cls):
        """Clean up any fouled transaction."""
        db.session.remove()
        db.drop_all()

    def test_message_creation(self):
        """Does creating a message work?"""
        msg = Message(text="Hello world!", user_id=self.user.id)
        db.session.add(msg)
        db.session.commit()

        self.assertEqual(len(self.user.messages), 1)
        self.assertEqual(self.user.messages[0].text, "Hello world!")

    def test_message_user_association(self):
        """Is the message correctly associated with the user?"""
        msg = Message(text="Another message", user_id=self.user.id)
        db.session.add(msg)
        db.session.commit()

        # Fetch the message back
        fetched_msg = Message.query.filter_by(text="Another message").first()
        self.assertIsNotNone(fetched_msg)
        self.assertEqual(fetched_msg.user_id, self.user.id)
        self.assertEqual(fetched_msg.user, self.user)

