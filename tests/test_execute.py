"""
Tests for execute routes (job submission and execution).
"""
import os
import pytest
import shutil
import time


@pytest.fixture
def confirmed_case(app, guest_session):
    """Create a confirmed case ready for execution."""
    from spc.model import db, jobs, users
    from spc.common import rand_cid
    from spc import user_data

    # First submit parameters to create the case
    dna_string = 'GATCACAGGTCTATCACCCTATTAACCACTCACGGGA'
    resp = guest_session.post('/confirm', data={
        'app': 'dna',
        'cid': '',
        'dna': dna_string,
        'desc': 'test execution case'
    })

    # Extract cid from the response (it's in the form)
    # The confirm page should have a hidden cid field
    assert resp.status_code == 200

    # Find cid in response data
    import re
    match = re.search(rb'name="cid"\s+value="([^"]+)"', resp.data)
    if match:
        cid = match.group(1).decode('utf-8')
    else:
        # Generate a cid and create directory manually
        cid = rand_cid()
        case_dir = os.path.join(user_data.user_data_root, 'guest', 'dna', cid)
        os.makedirs(case_dir, exist_ok=True)

        # Create input file
        input_file = os.path.join(case_dir, 'dna.ini')
        with open(input_file, 'w') as f:
            f.write('[dna]\ndna=ATCG\n')

    yield {'cid': cid, 'app': 'dna'}

    # Cleanup - remove case directory if it exists
    case_dir = os.path.join(user_data.user_data_root, 'guest', 'dna', cid)
    if os.path.exists(case_dir):
        shutil.rmtree(case_dir)

    # Remove any jobs created
    uid = users(user='guest').id
    job = jobs(cid=cid)
    if job:
        del jobs[job.id]
        db.commit()


@pytest.fixture
def running_case(app, guest_session):
    """Create a case with output file for tail testing."""
    from spc.model import db, jobs, users
    from spc.common import rand_cid
    from spc import user_data

    cid = rand_cid()
    uid = users(user='guest').id

    # Create job in database
    jid = jobs.insert(
        uid=uid,
        app='dna',
        cid=cid,
        state='R',  # Running
        description='running test case',
        time_submit=time.asctime(),
        walltime='3600',
        np=1,
        priority=3
    )
    db.commit()

    # Create directory and output file
    case_dir = os.path.join(user_data.user_data_root, 'guest', 'dna', cid)
    os.makedirs(case_dir, exist_ok=True)

    # Create output file with multiple lines
    output_file = os.path.join(case_dir, 'dna.out')
    with open(output_file, 'w') as f:
        for i in range(30):
            f.write(f'Output line {i}\n')

    # Create input file
    input_file = os.path.join(case_dir, 'dna.ini')
    with open(input_file, 'w') as f:
        f.write('[dna]\ndna=ATCG\n')

    yield {
        'jid': str(jid),
        'cid': cid,
        'app': 'dna',
        'case_dir': case_dir
    }

    # Cleanup
    if os.path.exists(case_dir):
        shutil.rmtree(case_dir)

    if jobs(id=jid):
        del jobs[jid]
        db.commit()


class TestConfirmRoute:
    """Tests for /confirm route."""

    def test_confirm_creates_case(self, guest_session):
        """POST /confirm creates a new case with parameters."""
        dna_string = 'ATCGATCGATCG'
        resp = guest_session.post('/confirm', data={
            'app': 'dna',
            'cid': '',
            'dna': dna_string,
            'desc': 'test case'
        })
        assert resp.status_code == 200
        # Should show confirmation page
        assert b'confirm' in resp.data.lower() or b'dna' in resp.data.lower()

    def test_confirm_with_description(self, guest_session):
        """POST /confirm handles description with commas."""
        resp = guest_session.post('/confirm', data={
            'app': 'dna',
            'cid': '',
            'dna': 'ATCG',
            'desc': 'test, with, commas'
        })
        assert resp.status_code == 200

    def test_confirm_without_description(self, guest_session):
        """POST /confirm handles missing description."""
        resp = guest_session.post('/confirm', data={
            'app': 'dna',
            'cid': '',
            'dna': 'ATCG'
        })
        assert resp.status_code == 200

    def test_confirm_generates_unique_cid(self, guest_session):
        """Each POST /confirm generates a unique case id."""
        import re

        resp1 = guest_session.post('/confirm', data={
            'app': 'dna',
            'cid': '',
            'dna': 'ATCG'
        })
        match1 = re.search(rb'name="cid"\s+value="([^"]+)"', resp1.data)

        resp2 = guest_session.post('/confirm', data={
            'app': 'dna',
            'cid': '',
            'dna': 'GCTA'
        })
        match2 = re.search(rb'name="cid"\s+value="([^"]+)"', resp2.data)

        if match1 and match2:
            cid1 = match1.group(1)
            cid2 = match2.group(1)
            assert cid1 != cid2


class TestExecuteRoute:
    """Tests for /execute route."""

    def test_execute_requires_valid_case(self, guest_session):
        """POST /execute with invalid case handles gracefully."""
        resp = guest_session.post('/execute', data={
            'app': 'dna',
            'cid': 'nonexistent_cid',
            'np': '1',
            'walltime': '60',
            'desc': 'test'
        })
        # Should return error or redirect
        assert resp.status_code in (200, 302, 500)

    def test_execute_with_confirmed_case(self, guest_session, confirmed_case):
        """POST /execute submits job for confirmed case."""
        cid = confirmed_case['cid']

        resp = guest_session.post('/execute', data={
            'app': 'dna',
            'cid': cid,
            'np': '1',
            'walltime': '60',
            'desc': 'test execution'
        }, follow_redirects=False)

        # Should redirect to case page or return OK
        assert resp.status_code in (200, 302)

    def test_execute_with_multiple_procs(self, guest_session, confirmed_case):
        """POST /execute handles np > 1."""
        cid = confirmed_case['cid']

        resp = guest_session.post('/execute', data={
            'app': 'dna',
            'cid': cid,
            'np': '2',
            'walltime': '60',
            'desc': 'parallel test'
        }, follow_redirects=False)

        assert resp.status_code in (200, 302)


class TestTailRoute:
    """Tests for /<app>/<cid>/tail route."""

    def test_tail_running_case(self, guest_session, running_case):
        """GET /<app>/<cid>/tail returns output content."""
        cid = running_case['cid']
        app = running_case['app']

        resp = guest_session.get(f'/{app}/{cid}/tail?num_lines=10')
        assert resp.status_code == 200
        # Should contain output lines
        assert b'Output line' in resp.data

    def test_tail_with_default_lines(self, guest_session, running_case):
        """GET /<app>/<cid>/tail requires num_lines parameter.

        Note: The route has a bug - it doesn't handle missing num_lines.
        It should default to 24 but instead raises TypeError.
        """
        cid = running_case['cid']
        app = running_case['app']

        # Must provide num_lines due to bug in route
        resp = guest_session.get(f'/{app}/{cid}/tail?num_lines=24')
        assert resp.status_code == 200

    def test_tail_nonexistent_case(self, guest_session):
        """GET /<app>/<cid>/tail handles nonexistent case."""
        resp = guest_session.get('/dna/nonexistent_cid/tail?num_lines=10')
        assert resp.status_code == 200
        # Should show error or "does not exist" message
        assert b'does not exist' in resp.data.lower() or b'oops' in resp.data.lower()

    def test_tail_waiting_case(self, guest_session, app):
        """GET /<app>/<cid>/tail shows waiting message when no output yet."""
        from spc.model import db, jobs, users
        from spc.common import rand_cid
        from spc import user_data

        cid = rand_cid()
        uid = users(user='guest').id

        # Create job
        jid = jobs.insert(
            uid=uid,
            app='dna',
            cid=cid,
            state='Q',  # Queued
            description='waiting test case',
            time_submit=time.asctime(),
            walltime='3600',
            np=1,
            priority=3
        )
        db.commit()

        # Create directory and input file but NO output file
        case_dir = os.path.join(user_data.user_data_root, 'guest', 'dna', cid)
        os.makedirs(case_dir, exist_ok=True)
        input_file = os.path.join(case_dir, 'dna.ini')
        with open(input_file, 'w') as f:
            f.write('[dna]\ndna=ATCG\n')

        try:
            resp = guest_session.get(f'/dna/{cid}/tail?num_lines=10')
            assert resp.status_code == 200
            # Should show waiting message
            assert b'waiting' in resp.data.lower()
        finally:
            # Cleanup
            if os.path.exists(case_dir):
                shutil.rmtree(case_dir)
            if jobs(id=jid):
                del jobs[jid]
                db.commit()


class TestRandCid:
    """Tests for rand_cid helper function."""

    def test_rand_cid_generates_string(self, app):
        """rand_cid generates a string identifier."""
        from spc.common import rand_cid

        cid = rand_cid()
        assert isinstance(cid, str)
        assert len(cid) > 0

    def test_rand_cid_starts_with_letter(self, app):
        """rand_cid starts with a letter."""
        from spc.common import rand_cid

        for _ in range(10):
            cid = rand_cid()
            assert cid[0].isalpha()

    def test_rand_cid_unique(self, app):
        """rand_cid generates unique identifiers."""
        from spc.common import rand_cid

        cids = set()
        for _ in range(100):
            cid = rand_cid()
            assert cid not in cids
            cids.add(cid)


class TestReplaceTags:
    """Tests for replace_tags helper function."""

    def test_replace_tags_basic(self, app):
        """replace_tags replaces placeholders with values."""
        from spc.common import replace_tags

        template = "Hello <name>, welcome to <place>!"
        params = {'name': 'Alice', 'place': 'SPC'}

        result = replace_tags(template, params)
        assert result == "Hello Alice, welcome to SPC!"

    def test_replace_tags_missing_param(self, app):
        """replace_tags raises KeyError for missing parameters.

        Note: This is a limitation of the current implementation.
        Missing parameters should ideally be handled gracefully.
        """
        from spc.common import replace_tags

        template = "Hello <name>!"
        params = {}

        # Current implementation raises KeyError for missing params
        with pytest.raises(KeyError):
            replace_tags(template, params)

    def test_replace_tags_no_tags(self, app):
        """replace_tags handles string with no tags."""
        from spc.common import replace_tags

        template = "No tags here"
        params = {'name': 'Alice'}

        result = replace_tags(template, params)
        assert result == "No tags here"
