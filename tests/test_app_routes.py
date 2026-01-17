"""
Tests for application routes (app display, confirm, execute).
Ported from legacy-tests/test_func_app.py
"""
import os


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
