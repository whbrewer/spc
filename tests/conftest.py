"""
Pytest configuration and fixtures for SPC tests.
"""
import hashlib
import os
import shutil
import sys
import tempfile

import pytest

# Add src to path so we can import spc modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture(scope='session')
def test_db_dir():
    """Create a temporary database directory for the test session."""
    tmpdir = tempfile.mkdtemp(prefix='spc_test_db_')
    yield tmpdir
    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.fixture(scope='session')
def app(test_db_dir):
    """Create and configure the Flask application for testing."""
    # Configure before importing spc modules
    from spc import config
    config.dbdir = test_db_dir
    config.db = 'test_spc.db'
    config.uri = 'sqlite://' + config.db
    config.auth = True
    config.np = 1
    config.server = 'testing'

    # Initialize the database
    from spc import migrate
    dal = migrate.dal(uri=config.uri, migrate=True)

    # Add default groups
    admin_gid = dal.db.groups.insert(name="admin")
    guest_gid = dal.db.groups.insert(name="guest")

    # Add admin and guest users
    admin_hash = hashlib.sha256("admin".encode('utf-8')).hexdigest()
    dal.db.users.insert(user="admin", passwd=admin_hash, gid=admin_gid)
    guest_hash = hashlib.sha256("guest".encode('utf-8')).hexdigest()
    dal.db.users.insert(user="guest", passwd=guest_hash, gid=guest_gid)

    # Add default DNA app
    dal.db.apps.insert(
        name="dna",
        description="Compute reverse complement, GC content, and codon analysis",
        category="bioinformatics",
        language="python",
        input_format="ini",
        command="<rel_apps_path>/dna/dna"
    )
    dal.db.plots.insert(id=1, appid=1, ptype="flot-cat", title="Dinucleotides")
    dal.db.plots.insert(id=2, appid=1, ptype="flot-cat", title="Nucleotides")
    dal.db.datasource.insert(filename="din.out", cols="1:2", pltid=1, data_def='{label: "Dinucleotides"}')
    dal.db.datasource.insert(filename="nucs.out", cols="1:2", pltid=2, data_def='{label: "Nucleotides"}')

    # Activate DNA app for admin and guest
    dal.db.app_user.insert(appid=1, uid=1)
    dal.db.app_user.insert(appid=1, uid=2)

    dal.db.commit()

    # Now import and configure Flask app
    from spc import main as spc_main
    spc_main.init_config_options()
    spc_main.load_apps()
    spc_main.register_routes()

    spc_main.app.testing = True
    yield spc_main.app


@pytest.fixture
def client(app):
    """Create a test client for making requests."""
    return app.test_client()


@pytest.fixture
def guest_session(client):
    """Create a test client logged in as guest."""
    client.post('/login', data={'user': 'guest', 'passwd': 'guest'})
    return client


@pytest.fixture
def admin_session(client):
    """Create a test client logged in as admin."""
    client.post('/login', data={'user': 'admin', 'passwd': 'admin'})
    return client


@pytest.fixture
def random_user():
    """Generate a random username for registration tests."""
    from spc.common import rand_cid
    return rand_cid()
