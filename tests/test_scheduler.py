"""
Unit tests for the job scheduler.
Ported from legacy-tests/test_unit_scheduler.py
"""
import pytest


class TestScheduler:
    """Tests for the Scheduler class."""

    @pytest.fixture
    def scheduler(self, app):
        """Create a scheduler instance for testing."""
        from spc.scheduler import Scheduler
        return Scheduler()

    def test_qsub(self, scheduler):
        """Test submitting a job to the queue."""
        app = "dna"
        cid = "TEST00"
        uid = 1
        cmd = "echo test"
        np = 1
        priority = 2
        walltime = "3600"
        desc = "test qsub"

        jid = scheduler.qsub(app, cid, uid, cmd, np, priority, walltime, desc)

        # Job ID should be returned as a string
        assert jid is not None
        assert int(jid) > 0

    def test_qstat(self, scheduler):
        """Test getting queue status."""
        # Get count of queued jobs
        count = scheduler.qstat()
        assert isinstance(count, int)
        assert count >= 0

    def test_qdel(self, scheduler):
        """Test deleting a job from the queue."""
        # First submit a job
        app = "dna"
        cid = "TESTDEL"
        uid = 1
        cmd = "echo test"
        np = 1
        priority = 1
        walltime = "3600"
        desc = "test qdel"

        jid = scheduler.qsub(app, cid, uid, cmd, np, priority, walltime, desc)

        # Now delete it
        scheduler.qdel(int(jid))

        # Verify it's deleted by checking the database
        from pydal import DAL
        from spc import config
        db = DAL(config.uri, auto_import=True, migrate=False, folder=config.dbdir)
        job = db.jobs(int(jid))
        db.close()

        assert job is None

    def test_qfront_empty(self, scheduler):
        """Test qfront returns None when queue is empty."""
        # Clear any existing queued jobs first
        from pydal import DAL
        from spc import config
        db = DAL(config.uri, auto_import=True, migrate=False, folder=config.dbdir)
        db(db.jobs.state == 'Q').delete()
        db.commit()
        db.close()

        # Now qfront should return None
        result = scheduler.qfront()
        # Could be None or no jobs
        assert result is None or result == 0 or result is False
