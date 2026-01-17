"""
Tests for login and registration routes.
Ported from legacy-tests/test_func_login.py
"""
import pytest


class TestLogin:
    """Tests for the /login route."""

    def test_login_page_loads(self, client):
        """GET /login returns the login page."""
        resp = client.get('/login')
        assert resp.status_code == 200

    def test_login_valid_credentials(self, client):
        """POST /login with valid credentials redirects."""
        resp = client.post('/login', data={'user': 'guest', 'passwd': 'guest'})
        # Successful login redirects (302)
        assert resp.status_code == 302

    def test_login_invalid_credentials(self, client):
        """POST /login with invalid credentials shows error."""
        resp = client.post('/login', data={'user': 'guest', 'passwd': 'wrongpassword'})
        assert resp.status_code == 200
        assert b'failed' in resp.data.lower() or b'invalid' in resp.data.lower()

    def test_login_missing_user_field(self, client):
        """POST /login with missing user field shows error message."""
        resp = client.post('/login', data={'passwd': 'guest'})
        assert resp.status_code == 200
        assert b'failed' in resp.data.lower()

    def test_login_missing_password_field(self, client):
        """POST /login with missing password field shows error message."""
        resp = client.post('/login', data={'user': 'guest'})
        assert resp.status_code == 200
        assert b'failed' in resp.data.lower()

    def test_login_empty_fields(self, client):
        """POST /login with empty fields shows error message."""
        resp = client.post('/login', data={'user': '', 'passwd': ''})
        assert resp.status_code == 200
        assert b'failed' in resp.data.lower()

    def test_login_admin(self, client):
        """POST /login as admin with valid credentials redirects."""
        resp = client.post('/login', data={'user': 'admin', 'passwd': 'admin'})
        assert resp.status_code == 302

    def test_login_admin_wrong_password(self, client):
        """POST /login as admin with wrong password fails."""
        resp = client.post('/login', data={'user': 'admin', 'passwd': 'wrongpassword'})
        assert resp.status_code == 200


class TestLogout:
    """Tests for the /logout route."""

    def test_logout(self, guest_session):
        """GET /logout logs out the user."""
        resp = guest_session.get('/logout')
        assert resp.status_code == 200


class TestRegistration:
    """Tests for user registration."""

    def test_register_page_loads(self, client):
        """GET /register returns the registration page."""
        resp = client.get('/register')
        assert resp.status_code == 200

    def test_register_new_user(self, client, random_user):
        """POST /register creates a new user."""
        resp = client.post('/register', data={
            'user': random_user,
            'email': 'test@spc.com',
            'password1': 'TestPass123',
            'password2': 'TestPass123'
        })
        # Successful registration redirects
        assert resp.status_code == 302

    def test_register_existing_user(self, client):
        """POST /register with existing username fails."""
        # Try to register as 'guest' which already exists
        resp = client.post('/register', data={
            'user': 'guest',
            'email': 'test@spc.com',
            'password1': 'TestPass123',
            'password2': 'TestPass123'
        })
        # Should return 200 with error message, not redirect
        assert resp.status_code == 200

    def test_check_user_exists(self, client):
        """POST /check_user returns 'true' for existing user."""
        resp = client.post('/check_user', data={'user': 'admin'})
        assert resp.status_code == 200
        assert resp.get_data(as_text=True) == 'true'

    def test_check_user_not_exists(self, client):
        """POST /check_user returns 'false' for non-existing user."""
        resp = client.post('/check_user', data={'user': 'nonexistent_user_xyz789'})
        assert resp.status_code == 200
        assert resp.get_data(as_text=True) == 'false'


class TestPasswordChange:
    """Tests for password change functionality."""

    def test_change_password(self, client, random_user):
        """POST /account/change_password changes the password."""
        # First register the user
        client.post('/register', data={
            'user': random_user,
            'email': 'test@spc.com',
            'password1': 'OldPass123',
            'password2': 'OldPass123'
        })

        # Now change the password
        resp = client.post('/account/change_password', data={
            'user': random_user,
            'opasswd': 'OldPass123',
            'npasswd1': 'NewPass456',
            'npasswd2': 'NewPass456'
        })
        assert resp.status_code == 200
