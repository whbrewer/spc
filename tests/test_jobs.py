"""
Tests for job management routes.
Tests the /jobs endpoints for listing, starring, sharing, and deleting jobs.
"""
import os
import pytest
import time


@pytest.fixture
def test_job(app, guest_session):
    """Create a test job in the database and return its info."""
    from spc.model import db, jobs, users
    from spc.common import rand_cid

    uid = users(user='guest').id
    cid = rand_cid()

    jid = jobs.insert(
        uid=uid,
        app='dna',
        cid=cid,
        state='C',  # Completed
        description='test job',
        time_submit=time.asctime(),
        walltime='3600',
        np=1,
        priority=3
    )
    db.commit()

    # Return jid as string since forms send strings
    yield {'jid': str(jid), 'cid': cid, 'app': 'dna', 'uid': uid}

    # Cleanup: delete the job if it still exists
    if jobs(id=jid):
        del jobs[jid]
        db.commit()


@pytest.fixture
def multiple_test_jobs(app, guest_session):
    """Create multiple test jobs for testing batch operations."""
    from spc.model import db, jobs, users
    from spc.common import rand_cid

    uid = users(user='guest').id
    created_jobs = []
    jids_for_cleanup = []

    for i in range(3):
        cid = rand_cid()
        jid = jobs.insert(
            uid=uid,
            app='dna',
            cid=cid,
            state='C',
            description=f'test job {i}',
            time_submit=time.asctime(),
            walltime='3600',
            np=1,
            priority=3
        )
        created_jobs.append({'jid': str(jid), 'cid': cid})
        jids_for_cleanup.append(jid)

    db.commit()

    yield created_jobs

    # Cleanup
    for jid in jids_for_cleanup:
        if jobs(id=jid):
            del jobs[jid]
    db.commit()


class TestJobsList:
    """Tests for /jobs listing routes."""

    def test_jobs_page_loads(self, guest_session):
        """GET /jobs returns the jobs list page."""
        resp = guest_session.get('/jobs')
        assert resp.status_code == 200

    def test_jobs_page_shows_jobs(self, guest_session, test_job):
        """GET /jobs shows existing jobs."""
        resp = guest_session.get('/jobs')
        assert resp.status_code == 200
        # The job's case ID should appear in the response
        assert test_job['cid'].encode() in resp.data

    def test_jobs_with_n_param(self, guest_session, multiple_test_jobs):
        """GET /jobs?n=2 limits the number of results."""
        resp = guest_session.get('/jobs?n=2')
        assert resp.status_code == 200

    def test_jobs_search_by_app(self, guest_session, test_job):
        """GET /jobs?q=app:dna filters by app name."""
        resp = guest_session.get('/jobs?q=app:dna')
        assert resp.status_code == 200

    def test_jobs_search_by_cid(self, guest_session, test_job):
        """GET /jobs?q=cid:XXX filters by case ID."""
        resp = guest_session.get(f'/jobs?q=cid:{test_job["cid"][:3]}')
        assert resp.status_code == 200

    def test_jobs_search_by_state(self, guest_session, test_job):
        """GET /jobs?q=state:C filters by job state."""
        resp = guest_session.get('/jobs?q=state:C')
        assert resp.status_code == 200

    def test_jobs_search_general(self, guest_session, test_job):
        """GET /jobs?q=test performs general search."""
        resp = guest_session.get('/jobs?q=test')
        assert resp.status_code == 200

    def test_jobs_starred_filter(self, guest_session):
        """GET /jobs?starred=1 filters starred jobs."""
        resp = guest_session.get('/jobs?starred=1')
        assert resp.status_code == 200

    def test_jobs_shared_filter(self, guest_session):
        """GET /jobs?shared=1 filters shared jobs."""
        resp = guest_session.get('/jobs?shared=1')
        assert resp.status_code == 200


class TestJobsNew:
    """Tests for /jobs/new route."""

    def test_jobs_new_requires_app(self, guest_session):
        """GET /jobs/new without app redirects to myapps."""
        resp = guest_session.get('/jobs/new')
        # Should redirect to /myapps if no app specified
        assert resp.status_code == 302

    def test_jobs_new_with_app_and_cid(self, guest_session, test_job):
        """GET /jobs/new?app=dna&cid=XXX loads the app form."""
        # Note: /jobs/new requires cid to be set (even empty string)
        # due to a bug where cid=None causes re.search to fail
        resp = guest_session.get(f'/jobs/new?app=dna&cid={test_job["cid"]}')
        assert resp.status_code == 200

    def test_jobs_new_restart_case(self, guest_session, test_job):
        """GET /jobs/new?app=dna&cid=XXX restarts from existing case."""
        resp = guest_session.get(f'/jobs/new?app=dna&cid={test_job["cid"]}')
        assert resp.status_code == 200


class TestJobsStar:
    """Tests for starring/unstarring jobs."""

    def test_star_job(self, guest_session, test_job):
        """POST /jobs/star stars a job."""
        resp = guest_session.post('/jobs/star', data={'jid': test_job['jid']})
        assert resp.status_code == 302  # Redirects to /jobs

        # Verify job is starred by checking the database
        from spc.model import db, jobs
        db.commit()  # Ensure we see the latest data
        job = db(db.jobs.id == int(test_job['jid'])).select().first()
        assert job is not None
        assert job.starred == "True"

    def test_unstar_job(self, guest_session, test_job):
        """POST /jobs/unstar unstars a job."""
        # First star it
        guest_session.post('/jobs/star', data={'jid': test_job['jid']})

        # Then unstar it
        resp = guest_session.post('/jobs/unstar', data={'jid': test_job['jid']})
        assert resp.status_code == 302

        # Verify job is unstarred
        from spc.model import db, jobs
        db.commit()
        job = db(db.jobs.id == int(test_job['jid'])).select().first()
        assert job is not None
        assert job.starred == "False"


class TestJobsShare:
    """Tests for sharing/unsharing jobs."""

    def test_share_job(self, guest_session, test_job):
        """POST /jobs/share shares a job."""
        resp = guest_session.post('/jobs/share', data={'jid': test_job['jid']})
        assert resp.status_code == 302

        # Verify job is shared
        from spc.model import db, jobs
        db.commit()
        job = db(db.jobs.id == int(test_job['jid'])).select().first()
        assert job is not None
        assert job.shared == "True"

    def test_unshare_job(self, guest_session, test_job):
        """POST /jobs/unshare unshares a job."""
        # First share it
        guest_session.post('/jobs/share', data={'jid': test_job['jid']})

        # Then unshare it
        resp = guest_session.post('/jobs/unshare', data={'jid': test_job['jid']})
        assert resp.status_code == 302

        # Verify job is unshared
        from spc.model import db, jobs
        db.commit()
        job = db(db.jobs.id == int(test_job['jid'])).select().first()
        assert job is not None
        assert job.shared == "False"

    def test_shared_jobs_page(self, guest_session, test_job):
        """GET /jobs/shared shows shared jobs."""
        # Share the job first
        guest_session.post('/jobs/share', data={'jid': test_job['jid']})

        resp = guest_session.get('/jobs/shared')
        assert resp.status_code == 200


class TestJobsAnnotate:
    """Tests for annotating jobs."""

    def test_annotate_job(self, guest_session, test_job):
        """POST /jobs/annotate updates job description."""
        new_desc = "updated description, with labels"
        resp = guest_session.post('/jobs/annotate', data={
            'cid': test_job['cid'],
            'description': new_desc
        })
        assert resp.status_code == 302

        # Verify description was updated
        from spc.model import jobs
        job = jobs(cid=test_job['cid'])
        assert 'updated description' in job.description


class TestJobsDelete:
    """Tests for deleting jobs."""

    def test_delete_job(self, guest_session, test_job):
        """POST /jobs/delete/<jid> deletes a job."""
        resp = guest_session.post(f'/jobs/delete/{test_job["jid"]}', data={
            'app': test_job['app'],
            'cid': test_job['cid']
        })
        assert resp.status_code == 302

        # Verify job is deleted
        from spc.model import jobs
        job = jobs(id=test_job['jid'])
        assert job is None

    def test_delete_selected_cases(self, guest_session, multiple_test_jobs):
        """POST /jobs/delete_selected_cases deletes multiple jobs."""
        # Build the selected_cases string (jid1:jid2:jid3:)
        selected = ':'.join(str(j['jid']) for j in multiple_test_jobs) + ':'

        resp = guest_session.post('/jobs/delete_selected_cases', data={
            'selected_cases': selected
        })
        assert resp.status_code == 302

        # Verify jobs are deleted
        from spc.model import jobs
        for job in multiple_test_jobs:
            assert jobs(id=job['jid']) is None


class TestJobsStop:
    """Tests for stopping jobs."""

    def test_stop_job(self, guest_session, test_job):
        """POST /jobs/stop stops a job and updates state to X."""
        resp = guest_session.post('/jobs/stop', data={
            'app': test_job['app'],
            'cid': test_job['cid'],
            'jid': test_job['jid']
        })
        # Should redirect to case page
        assert resp.status_code == 302

        # Verify job state is updated to stopped
        from spc.model import db, jobs
        db.commit()
        job = db(db.jobs.id == int(test_job['jid'])).select().first()
        assert job is not None
        assert job.state == 'X'


class TestJobsAdmin:
    """Tests for admin-only job routes."""

    def test_jobs_all_requires_admin(self, guest_session):
        """GET /jobs/all requires admin privileges."""
        resp = guest_session.get('/jobs/all')
        assert resp.status_code == 200
        assert b'admin' in resp.data.lower() or b'error' in resp.data.lower()

    def test_jobs_all_as_admin(self, admin_session, test_job):
        """GET /jobs/all works for admin."""
        resp = admin_session.get('/jobs/all')
        assert resp.status_code == 200

    def test_jobs_search_all_users_as_admin(self, admin_session, test_job):
        """GET /jobs?q=user:all shows all users' jobs for admin."""
        resp = admin_session.get('/jobs?q=user:all')
        assert resp.status_code == 200
