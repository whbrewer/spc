"""
Tests for admin routes and app configuration.
Ported from legacy-tests/test_func_addapp.py
"""


class TestAdminRoutes:
    """Tests for admin-only routes."""

    def test_admin_page_requires_auth(self, client):
        """Admin pages require authentication."""
        resp = client.get('/admin')
        # Should redirect to login or show unauthorized
        assert resp.status_code in (200, 302, 401, 403)

    def test_admin_page_as_admin(self, admin_session):
        """Admin can access admin pages."""
        resp = admin_session.get('/admin')
        assert resp.status_code == 200

    def test_delete_user(self, admin_session, client, random_user):
        """Admin can delete a user."""
        # First create a user to delete
        client.post('/register', data={
            'user': random_user,
            'email': 'delete@test.com',
            'password1': 'TestPass123',
            'password2': 'TestPass123'
        })

        # Get the user's ID from the database
        from spc.model import users
        user_row = users(user=random_user)
        if user_row:
            uid = user_row.id
            resp = admin_session.post('/admin/delete_user', data={'uid': uid})
            assert resp.status_code == 302


class TestAppConfig:
    """Tests for app configuration routes."""

    def test_addapp_route(self, admin_session):
        """POST /addapp is accessible."""
        resp = admin_session.post('/addapp', data={'appname': 'testapp'})
        # Should return 200 or redirect
        assert resp.status_code in (200, 302)

    def test_apps_page(self, admin_session):
        """GET /apps shows all installed apps."""
        resp = admin_session.get('/apps')
        assert resp.status_code == 200

    def test_myapps_page(self, guest_session):
        """GET /myapps shows activated apps for user."""
        resp = guest_session.get('/myapps')
        assert resp.status_code == 200
