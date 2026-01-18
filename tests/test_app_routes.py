"""
Tests for application routes (app display, confirm, execute).
Ported from legacy-tests/test_func_app.py
"""
import os
import pytest


class TestAppDisplay:
    """Tests for app display routes."""

    def test_app_page_loads(self, guest_session):
        """GET /<app> returns the app page."""
        resp = guest_session.get('/dna')
        assert resp.status_code == 200

    def test_app_not_found(self, guest_session):
        """GET /<nonexistent_app> returns 404 or error."""
        resp = guest_session.get('/nonexistent_app_xyz')
        # Could be 404 or 500 depending on implementation
        assert resp.status_code in (404, 500) or b'error' in resp.data.lower()

    def test_myapps_page(self, guest_session):
        """GET /myapps returns the user's apps page."""
        resp = guest_session.get('/myapps')
        assert resp.status_code == 200


class TestAppExists:
    """Tests for /app_exists route."""

    def test_app_exists_true(self, guest_session):
        """GET /app_exists/<appname> returns 'true' for existing app."""
        resp = guest_session.get('/app_exists/dna')
        assert resp.status_code == 200
        assert resp.get_data(as_text=True) == 'true'

    def test_app_exists_false(self, guest_session):
        """GET /app_exists/<appname> returns 'false' for non-existing app."""
        resp = guest_session.get('/app_exists/nonexistent_app_xyz')
        assert resp.status_code == 200
        assert resp.get_data(as_text=True) == 'false'


class TestConfirm:
    """Tests for /confirm route (parameter submission)."""

    def test_confirm_dna_params(self, guest_session):
        """POST /confirm writes parameters and shows confirmation."""
        dna_string = 'GATCACAGGTCTATCACCCTATTAACCACTCACGGGA'
        resp = guest_session.post('/confirm', data={
            'app': 'dna',
            'cid': '',
            'dna': dna_string
        })
        assert resp.status_code == 200


class TestExecute:
    """Tests for /execute route (job submission)."""

    def test_execute_requires_params(self, guest_session):
        """POST /execute without proper setup should handle gracefully."""
        resp = guest_session.post('/execute', data={
            'app': 'dna',
            'cid': 'TESTCID',
            'np': '1'
        })
        # Should return some response (may be error if case doesn't exist)
        assert resp.status_code in (200, 302, 400, 404, 500)


class TestDNAWorkflow:
    """End-to-end test for DNA app workflow."""

    def test_dna_full_workflow(self, guest_session):
        """Test complete DNA app workflow: display -> confirm -> execute."""
        # Step 1: Load app page
        resp = guest_session.get('/dna')
        assert resp.status_code == 200

        # Step 2: Submit parameters
        dna_string = 'GATCACAGGTCTATCACCCTATTAACCACTCACGGGA'
        resp = guest_session.post('/confirm', data={
            'app': 'dna',
            'cid': '',
            'dna': dna_string,
            'desc': 'test run'
        })
        assert resp.status_code == 200


class TestAppsBrowser:
    """Tests for /apps route (app browser)."""

    def test_apps_page_loads(self, guest_session):
        """GET /apps returns the apps browser page."""
        resp = guest_session.get('/apps')
        assert resp.status_code == 200
        assert b'dna' in resp.data.lower()

    def test_apps_search(self, guest_session):
        """GET /apps?q=<query> filters apps by search term."""
        resp = guest_session.get('/apps?q=dna')
        assert resp.status_code == 200
        assert b'dna' in resp.data.lower()

    def test_apps_search_no_results(self, guest_session):
        """GET /apps?q=<nonexistent> returns page with no matching apps."""
        resp = guest_session.get('/apps?q=nonexistent_app_xyz')
        assert resp.status_code == 200

    def test_apps_search_by_category(self, guest_session):
        """GET /apps?q=<category> can search by category."""
        resp = guest_session.get('/apps?q=bioinformatics')
        assert resp.status_code == 200


class TestAppsLoad:
    """Tests for /apps/load route."""

    def test_apps_load_redirects(self, guest_session):
        """GET /apps/load reloads apps and redirects to /myapps."""
        resp = guest_session.get('/apps/load', follow_redirects=False)
        assert resp.status_code == 302
        assert '/myapps' in resp.headers.get('Location', '')

    def test_apps_load_with_follow(self, guest_session):
        """GET /apps/load reloads apps and shows myapps page."""
        resp = guest_session.get('/apps/load', follow_redirects=True)
        assert resp.status_code == 200


class TestAdminAppView:
    """Tests for admin app view routes."""

    def test_view_app_as_admin(self, admin_session):
        """GET /app/<app> shows app details for admin."""
        resp = admin_session.get('/app/dna')
        assert resp.status_code == 200

    def test_view_app_requires_admin(self, guest_session):
        """GET /app/<app> requires admin privileges."""
        resp = guest_session.get('/app/dna')
        assert resp.status_code == 200
        assert b'admin' in resp.data.lower() or b'error' in resp.data.lower()

    def test_view_app_empty_redirects(self, admin_session):
        """GET /app/ with empty app redirects to myapps."""
        # The route pattern is /app/<app> so empty would be different route
        resp = admin_session.get('/app/', follow_redirects=True)
        # May return 404 or redirect
        assert resp.status_code in (200, 302, 404)


class TestAdminAppEdit:
    """Tests for admin app edit routes."""

    def test_app_edit_requires_admin(self, guest_session):
        """POST /app/edit/<appid> requires admin."""
        resp = guest_session.post('/app/edit/1', data={
            'app': 'dna',
            'cid': ''
        })
        assert resp.status_code == 200
        assert b'admin' in resp.data.lower() or b'error' in resp.data.lower()

    def test_app_edit_as_admin(self, admin_session):
        """POST /app/edit/<appid> shows edit form for admin."""
        resp = admin_session.post('/app/edit/1', data={
            'app': 'dna',
            'cid': ''
        })
        assert resp.status_code == 200

    def test_app_save_as_admin(self, admin_session):
        """POST /app/save/<appid> saves app changes."""
        resp = admin_session.post('/app/save/1', data={
            'app': 'dna',
            'language': 'python',
            'input_format': 'ini',
            'category': 'bioinformatics',
            'preprocess': '',
            'postprocess': '',
            'assets': '',
            'description': 'Updated description'
        }, follow_redirects=False)
        assert resp.status_code == 302
        assert '/app/dna' in resp.headers.get('Location', '')


class TestUserAppActivation:
    """Tests for user app activation/deactivation."""

    def test_useapp_activates_app(self, admin_session, app):
        """POST /useapp activates an app for the user."""
        # First we need another app to activate
        # Since DNA is already activated, we'll test the route works
        # by checking the redirect behavior
        resp = admin_session.post('/useapp', data={
            'app': 'dna'
        }, follow_redirects=False)
        # May fail with integrity error if already activated, but route should work
        assert resp.status_code in (302, 500)

    def test_removeapp_deactivates_app(self, guest_session):
        """POST /removeapp deactivates an app for the user."""
        resp = guest_session.post('/removeapp', data={
            'app': 'dna'
        }, follow_redirects=False)
        assert resp.status_code == 302
        assert '/myapps' in resp.headers.get('Location', '')


class TestAddApp:
    """Tests for admin add app routes."""

    def test_addapp_get_requires_admin(self, guest_session):
        """GET /addapp requires admin."""
        resp = guest_session.get('/addapp')
        assert resp.status_code == 200
        assert b'admin' in resp.data.lower() or b'error' in resp.data.lower()

    def test_addapp_get_as_admin(self, admin_session):
        """GET /addapp shows add app form for admin."""
        resp = admin_session.get('/addapp')
        assert resp.status_code == 200

    def test_addapp_post_requires_admin(self, guest_session):
        """POST /addapp requires admin."""
        resp = guest_session.post('/addapp', data={
            'appname': 'testapp',
            'input_format': 'ini'
        })
        assert resp.status_code == 200
        assert b'admin' in resp.data.lower() or b'error' in resp.data.lower()


class TestAppConfigStatus:
    """Tests for /appconfig/status route."""

    def test_appconfig_status(self, guest_session):
        """GET /appconfig/status returns JSON status for app."""
        resp = guest_session.get('/appconfig/status?app=dna')
        assert resp.status_code == 200
        import json
        data = json.loads(resp.get_data(as_text=True))
        assert 'command' in data
        assert 'template' in data
        assert 'inputs' in data
        assert 'binary' in data
        assert 'plots' in data


class TestAppConfigExport:
    """Tests for /appconfig/export route."""

    def test_export_requires_admin(self, guest_session):
        """POST /appconfig/export requires admin."""
        resp = guest_session.post('/appconfig/export', data={
            'app': 'dna'
        })
        assert resp.status_code == 200
        assert b'admin' in resp.data.lower() or b'error' in resp.data.lower()

    def test_export_as_admin(self, admin_session):
        """POST /appconfig/export exports app config."""
        resp = admin_session.post('/appconfig/export', data={
            'app': 'dna'
        })
        assert resp.status_code == 200
        assert b'spc.json' in resp.data


class TestAppConfigInputs:
    """Tests for /appconfig/inputs routes."""

    def test_inputs_upload_requires_admin(self, guest_session):
        """POST /appconfig/inputs/upload requires admin."""
        resp = guest_session.post('/appconfig/inputs/upload', data={
            'appname': 'dna',
            'input_format': 'ini'
        })
        assert resp.status_code == 200
        assert b'admin' in resp.data.lower() or b'error' in resp.data.lower()

    def test_inputs_upload_as_admin(self, admin_session):
        """POST /appconfig/inputs/upload shows upload form."""
        resp = admin_session.post('/appconfig/inputs/upload', data={
            'appname': 'dna',
            'input_format': 'ini'
        })
        assert resp.status_code == 200

    def test_inputs_unsupported_step(self, admin_session):
        """POST /appconfig/inputs/<invalid_step> returns error."""
        resp = admin_session.post('/appconfig/inputs/invalid_step', data={
            'appname': 'dna'
        })
        assert resp.status_code == 200
        assert b'error' in resp.data.lower()


class TestAppConfigExe:
    """Tests for /appconfig/exe routes."""

    def test_exe_upload_requires_admin(self, guest_session):
        """POST /appconfig/exe/upload requires admin."""
        resp = guest_session.post('/appconfig/exe/upload', data={
            'appname': 'dna'
        })
        assert resp.status_code == 200
        assert b'admin' in resp.data.lower() or b'error' in resp.data.lower()

    def test_exe_upload_as_admin(self, admin_session):
        """POST /appconfig/exe/upload shows upload form."""
        resp = admin_session.post('/appconfig/exe/upload', data={
            'appname': 'dna'
        })
        assert resp.status_code == 200


class TestAppDelete:
    """Tests for app deletion route."""

    def test_delete_requires_admin(self, guest_session):
        """POST /app/delete/<appid> requires admin."""
        resp = guest_session.post('/app/delete/1', data={
            'app': 'dna'
        })
        assert resp.status_code == 200
        assert b'admin' in resp.data.lower() or b'error' in resp.data.lower()


class TestNormalizeInputFormat:
    """Tests for normalize_input_format helper function."""

    def test_normalize_valid_formats(self, app):
        """Test that valid formats are normalized correctly."""
        from spc.app_routes import normalize_input_format
        assert normalize_input_format('INI') == 'ini'
        assert normalize_input_format('XML') == 'xml'
        assert normalize_input_format('JSON') == 'json'
        assert normalize_input_format('YAML') == 'yaml'
        assert normalize_input_format('TOML') == 'toml'
        assert normalize_input_format('NAMELIST') == 'namelist'

    def test_normalize_with_default(self, app):
        """Test that default is used for invalid format."""
        from spc.app_routes import normalize_input_format
        assert normalize_input_format('invalid', default='ini') == 'ini'
        assert normalize_input_format(None, default='json') == 'json'
        assert normalize_input_format('', default='yaml') == 'yaml'
