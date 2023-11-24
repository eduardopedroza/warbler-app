from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///warbler_test'
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False  

class UserViewsTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        """Create test client, add sample data."""
        cls.client = app.test_client()

        db.create_all()
        User.query.delete()

        user1 = User.signup(username="user1", email="user1@test.com", password="password", image_url=None)
        db.session.commit()

        cls.user1 = User.query.filter_by(username="user1").first()

    @classmethod
    def tearDownClass(cls):
        """Clean up any fouled transaction."""
        db.session.remove()
        db.drop_all()

    def test_signup_page(self):
        """Can use access the signup page?"""
        with self.client as client:
            res = client.get("/signup")
            self.assertEqual(res.status_code, 200)
            self.assertIn('Sign up', res.get_data(as_text=True))

    def test_user_signup(self):
        """Does user signup work?"""
        with self.client as client:
            res = client.post("/signup", data={"username": "user2", "email": "user2@test.com", "password": "password2"}, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('user2', res.get_data(as_text=True))

    def test_user_login(self):
        """Does user login work?"""
        with self.client as client:
            res = client.post("/login", data={"username": "user1", "password": "password"}, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("user1", res.get_data(as_text=True))

    def test_invalid_user_login(self):
        """Does login fail with wrong credentials?"""
        with self.client as client:
            res = client.post("/login", data={"username": "user1", "password": "wrongpassword"}, follow_redirects=True)
            self.assertIn("Invalid credentials.", res.get_data(as_text=True))

    def test_logout(self):
        """Does logout work?"""
        with self.client as client:
            # First, login
            client.post("/login", data={"username": "user1", "password": "password"}, follow_redirects=True)
            # Then, logout
            res = client.get("/logout", follow_redirects=True)
            self.assertIn("Successfully Logged Out", res.get_data(as_text=True))
            self.assertIn("Sign up", res.get_data(as_text=True))

