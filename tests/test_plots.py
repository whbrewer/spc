"""
Tests for plot routes and Plot class functionality.
"""
import json
import os
import pytest
import shutil
import tempfile
import time


@pytest.fixture
def plot_case_with_data(app, guest_session):
    """Create a test case with plot data files."""
    from spc.model import db, jobs, users
    from spc.common import rand_cid
    from spc import user_data

    uid = users(user='guest').id
    cid = rand_cid()

    # Create job in database
    jid = jobs.insert(
        uid=uid,
        app='dna',
        cid=cid,
        state='C',
        description='test case for plotting',
        time_submit=time.asctime(),
        walltime='3600',
        np=1,
        priority=3
    )
    db.commit()

    # Create directory and data files
    case_dir = os.path.join(user_data.user_data_root, 'guest', 'dna', cid)
    os.makedirs(case_dir, exist_ok=True)

    # Create input file
    input_file = os.path.join(case_dir, 'dna.ini')
    with open(input_file, 'w') as f:
        f.write('[dna]\ndna=ATCG\n')

    # Create dinucleotide output file (for flot-cat plot)
    din_file = os.path.join(case_dir, 'din.out')
    with open(din_file, 'w') as f:
        f.write('# Dinucleotide frequencies\n')
        f.write('AA\t10\n')
        f.write('AT\t15\n')
        f.write('AC\t8\n')
        f.write('AG\t12\n')

    # Create nucleotide output file
    nucs_file = os.path.join(case_dir, 'nucs.out')
    with open(nucs_file, 'w') as f:
        f.write('# Nucleotide frequencies\n')
        f.write('A\t25\n')
        f.write('T\t30\n')
        f.write('C\t20\n')
        f.write('G\t25\n')

    # Create a generic data file for testing
    data_file = os.path.join(case_dir, 'data.dat')
    with open(data_file, 'w') as f:
        f.write('# Test data\n')
        for i in range(50):
            f.write(f'{i}\t{i*2}\t{i*3}\n')

    # Create CSV data file
    csv_file = os.path.join(case_dir, 'data.csv')
    with open(csv_file, 'w') as f:
        f.write('x,y,z\n')
        f.write('1,2,3\n')
        f.write('4,5,6\n')
        f.write('7,8,9\n')

    yield {
        'jid': str(jid),
        'cid': cid,
        'app': 'dna',
        'uid': uid,
        'case_dir': case_dir
    }

    # Cleanup
    if os.path.exists(case_dir):
        shutil.rmtree(case_dir)
    parent = os.path.dirname(case_dir)
    if os.path.exists(parent) and not os.listdir(parent):
        os.rmdir(parent)

    if jobs(id=jid):
        del jobs[jid]
        db.commit()


@pytest.fixture
def admin_plot_case(app, admin_session):
    """Create a test case owned by admin for plot testing."""
    from spc.model import db, jobs, users
    from spc.common import rand_cid
    from spc import user_data

    uid = users(user='admin').id
    cid = rand_cid()

    jid = jobs.insert(
        uid=uid,
        app='dna',
        cid=cid,
        state='C',
        description='admin plot test case',
        time_submit=time.asctime(),
        walltime='3600',
        np=1,
        priority=3
    )
    db.commit()

    case_dir = os.path.join(user_data.user_data_root, 'admin', 'dna', cid)
    os.makedirs(case_dir, exist_ok=True)

    # Create required files
    input_file = os.path.join(case_dir, 'dna.ini')
    with open(input_file, 'w') as f:
        f.write('[dna]\ndna=ATCG\n')

    din_file = os.path.join(case_dir, 'din.out')
    with open(din_file, 'w') as f:
        f.write('AA\t10\n')

    nucs_file = os.path.join(case_dir, 'nucs.out')
    with open(nucs_file, 'w') as f:
        f.write('A\t25\n')

    yield {
        'jid': str(jid),
        'cid': cid,
        'app': 'dna',
        'case_dir': case_dir
    }

    if os.path.exists(case_dir):
        shutil.rmtree(case_dir)
    parent = os.path.dirname(case_dir)
    if os.path.exists(parent) and not os.listdir(parent):
        os.rmdir(parent)

    if jobs(id=jid):
        del jobs[jid]
        db.commit()


class TestPlotClass:
    """Tests for the Plot class helper methods."""

    def test_get_data_two_columns(self, app, plot_case_with_data):
        """Plot.get_data returns data for two columns."""
        from spc.plots import Plot

        case_dir = plot_case_with_data['case_dir']
        data_file = os.path.join(case_dir, 'data.dat')

        p = Plot()
        result = p.get_data(data_file, 1, 2)

        assert isinstance(result, str)
        assert '[' in result  # Should be array format

    def test_get_data_single_column(self, app, plot_case_with_data):
        """Plot.get_data returns list for single column."""
        from spc.plots import Plot

        case_dir = plot_case_with_data['case_dir']
        data_file = os.path.join(case_dir, 'data.dat')

        p = Plot()
        result = p.get_data(data_file, 1)

        assert isinstance(result, list)
        assert len(result) > 0

    def test_get_data_with_line_range(self, app, plot_case_with_data):
        """Plot.get_data respects line range."""
        from spc.plots import Plot

        case_dir = plot_case_with_data['case_dir']
        data_file = os.path.join(case_dir, 'data.dat')

        p = Plot()
        result = p.get_data(data_file, 1, 2, line1=1, line2=10)

        assert isinstance(result, str)

    def test_get_data_negative_line_range(self, app, plot_case_with_data):
        """Plot.get_data handles negative line range (tail)."""
        from spc.plots import Plot

        case_dir = plot_case_with_data['case_dir']
        data_file = os.path.join(case_dir, 'data.dat')

        p = Plot()
        result = p.get_data(data_file, 1, 2, line1=-10, line2=1000)

        assert isinstance(result, str)

    def test_get_data_nonexistent_file(self, app):
        """Plot.get_data returns -1 for nonexistent file."""
        from spc.plots import Plot

        p = Plot()
        result = p.get_data('/nonexistent/file.dat', 1, 2)

        assert result == -1

    def test_get_csv_data(self, app, plot_case_with_data):
        """Plot.get_csv_data reads CSV files."""
        from spc.plots import Plot

        case_dir = plot_case_with_data['case_dir']
        csv_file = os.path.join(case_dir, 'data.csv')

        p = Plot()
        result = p.get_csv_data(csv_file)

        assert isinstance(result, list)
        assert len(result) == 4  # header + 3 rows
        assert result[0] == ['x', 'y', 'z']

    def test_get_csv_data_nonexistent(self, app):
        """Plot.get_csv_data returns -1 for nonexistent file."""
        from spc.plots import Plot

        p = Plot()
        result = p.get_csv_data('/nonexistent/file.csv')

        assert result == -1

    def test_get_raw_data(self, app, plot_case_with_data):
        """Plot.get_raw_data returns raw file lines.

        Note: The default line2=1e6 is a float which causes TypeError in slicing.
        We pass explicit integer values to avoid this bug.
        """
        from spc.plots import Plot

        case_dir = plot_case_with_data['case_dir']
        data_file = os.path.join(case_dir, 'data.dat')

        p = Plot()
        # Must pass integer for line2 due to bug in implementation
        result = p.get_raw_data(data_file, line1=1, line2=100)

        assert isinstance(result, list)
        assert len(result) > 0

    def test_get_raw_data_with_range(self, app, plot_case_with_data):
        """Plot.get_raw_data respects line range."""
        from spc.plots import Plot

        case_dir = plot_case_with_data['case_dir']
        data_file = os.path.join(case_dir, 'data.dat')

        p = Plot()
        result = p.get_raw_data(data_file, line1=1, line2=5)

        assert isinstance(result, list)
        assert len(result) <= 5

    def test_get_column_of_data(self, app, plot_case_with_data):
        """Plot.get_column_of_data returns single column."""
        from spc.plots import Plot

        case_dir = plot_case_with_data['case_dir']
        data_file = os.path.join(case_dir, 'data.dat')

        p = Plot()
        result = p.get_column_of_data(data_file, 1)

        assert isinstance(result, list)
        assert len(result) > 0

    def test_get_column_negative_line_range(self, app, plot_case_with_data):
        """Plot.get_column_of_data handles negative line range."""
        from spc.plots import Plot

        case_dir = plot_case_with_data['case_dir']
        data_file = os.path.join(case_dir, 'data.dat')

        p = Plot()
        result = p.get_column_of_data(data_file, 1, line1=-10, line2=1000)

        assert isinstance(result, list)

    def test_get_ticks(self, app, plot_case_with_data):
        """Plot.get_ticks returns tick data."""
        from spc.plots import Plot

        case_dir = plot_case_with_data['case_dir']
        din_file = os.path.join(case_dir, 'din.out')

        p = Plot()
        result = p.get_ticks(din_file, 1, 2)

        assert isinstance(result, str)
        assert '[' in result


class TestComputeStats:
    """Tests for compute_stats function."""

    def test_compute_stats_with_comments(self, app, plot_case_with_data):
        """compute_stats extracts comment lines."""
        from spc.plots import compute_stats

        case_dir = plot_case_with_data['case_dir']
        data_file = os.path.join(case_dir, 'data.dat')

        result = compute_stats(data_file)

        assert isinstance(result, str)
        # Should contain comment lines
        assert '#' in result or result == ''

    def test_compute_stats_nonexistent_file(self, app):
        """compute_stats returns empty string for nonexistent file."""
        from spc.plots import compute_stats

        result = compute_stats('/nonexistent/file.dat')

        assert result == ''


class TestPlotEditRoutes:
    """Tests for plot editing routes (admin only)."""

    def test_edit_plotdefs_requires_admin(self, guest_session):
        """GET /plots/edit requires admin."""
        resp = guest_session.get('/plots/edit?app=dna')
        assert resp.status_code == 200
        assert b'admin' in resp.data.lower() or b'error' in resp.data.lower()

    def test_edit_plotdefs_as_admin(self, admin_session):
        """GET /plots/edit shows plot definitions for admin."""
        resp = admin_session.get('/plots/edit?app=dna')
        assert resp.status_code == 200

    def test_edit_plot_requires_admin(self, guest_session):
        """GET /plots/edit/<pltid> requires admin."""
        resp = guest_session.get('/plots/edit/1')
        assert resp.status_code == 200
        assert b'admin' in resp.data.lower() or b'error' in resp.data.lower()

    def test_edit_plot_as_admin(self, admin_session):
        """GET /plots/edit/<pltid> shows edit form for admin."""
        resp = admin_session.get('/plots/edit/1')
        assert resp.status_code == 200

    def test_save_plot_requires_admin(self, guest_session):
        """POST /plots/edit/<pltid> requires admin."""
        resp = guest_session.post('/plots/edit/1', data={
            'app': 'dna',
            'title': 'Test Plot',
            'ptype': 'flot-cat',
            'options': ''
        })
        assert resp.status_code == 200
        assert b'admin' in resp.data.lower() or b'error' in resp.data.lower()

    def test_save_plot_as_admin(self, admin_session):
        """POST /plots/edit/<pltid> saves changes for admin."""
        resp = admin_session.post('/plots/edit/1', data={
            'app': 'dna',
            'title': 'Updated Title',
            'ptype': 'flot-cat',
            'options': ''
        }, follow_redirects=False)
        assert resp.status_code == 302
        assert '/plots/edit' in resp.headers.get('Location', '')


class TestPlotDeleteRoute:
    """Tests for plot deletion route."""

    def test_delete_plot_requires_admin(self, guest_session):
        """GET /plots/delete/<pltid> requires admin."""
        resp = guest_session.get('/plots/delete/999?app=dna')
        assert resp.status_code == 200
        assert b'admin' in resp.data.lower() or b'error' in resp.data.lower()


class TestDatasourceRoutes:
    """Tests for datasource management routes."""

    def test_get_datasources_requires_admin(self, guest_session):
        """GET /plots/<pltid>/datasources requires admin."""
        resp = guest_session.get('/plots/1/datasources?app=dna')
        assert resp.status_code == 200
        assert b'admin' in resp.data.lower() or b'error' in resp.data.lower()

    def test_get_datasources_as_admin(self, admin_session):
        """GET /plots/<pltid>/datasources shows datasources for admin."""
        resp = admin_session.get('/plots/1/datasources?app=dna')
        assert resp.status_code == 200

    def test_add_datasource_requires_admin(self, guest_session):
        """POST /plots/<pltid>/datasources requires admin."""
        resp = guest_session.post('/plots/1/datasources', data={
            'app': 'dna',
            'label': 'Test',
            'fn': 'test.out',
            'cols': '1:2',
            'line_range': '',
            'data_def': ''
        })
        assert resp.status_code == 200
        assert b'admin' in resp.data.lower() or b'error' in resp.data.lower()

    def test_edit_datasource_requires_admin(self, guest_session):
        """GET /plots/<pltid>/datasources/<dsid> requires admin."""
        resp = guest_session.get('/plots/1/datasources/1?app=dna')
        assert resp.status_code == 200
        assert b'admin' in resp.data.lower() or b'error' in resp.data.lower()

    def test_edit_datasource_as_admin(self, admin_session):
        """GET /plots/<pltid>/datasources/<dsid> shows edit form."""
        resp = admin_session.get('/plots/1/datasources/1?app=dna')
        assert resp.status_code == 200

    def test_save_datasource_requires_admin(self, guest_session):
        """POST /plots/<pltid>/datasources/<dsid> requires admin."""
        resp = guest_session.post('/plots/1/datasources/1', data={
            'app': 'dna',
            'label': 'Updated',
            'fn': 'test.out',
            'cols': '1:2',
            'line_range': '',
            'data_def': ''
        })
        assert resp.status_code == 200
        assert b'admin' in resp.data.lower() or b'error' in resp.data.lower()

    def test_save_datasource_as_admin(self, admin_session):
        """POST /plots/<pltid>/datasources/<dsid> saves changes."""
        resp = admin_session.post('/plots/1/datasources/1', data={
            'app': 'dna',
            'label': 'Updated Label',
            'fn': 'din.out',
            'cols': '1:2',
            'line_range': '',
            'data_def': '{label: "Test"}'
        }, follow_redirects=False)
        assert resp.status_code == 302

    def test_delete_datasource_requires_admin(self, guest_session):
        """POST /plots/datasource_delete requires admin."""
        resp = guest_session.post('/plots/datasource_delete', data={
            'app': 'dna',
            'pltid': '1',
            'dsid': '999'
        })
        assert resp.status_code == 200
        assert b'admin' in resp.data.lower() or b'error' in resp.data.lower()


class TestCreatePlotRoute:
    """Tests for plot creation route."""

    def test_create_plot_requires_admin(self, guest_session):
        """POST /plots/create requires admin."""
        resp = guest_session.post('/plots/create', data={
            'app': 'dna',
            'ptype': 'flot-line',
            'title': 'New Plot',
            'options': ''
        })
        assert resp.status_code == 200
        assert b'admin' in resp.data.lower() or b'error' in resp.data.lower()

    def test_create_plot_as_admin(self, admin_session):
        """POST /plots/create creates new plot for admin."""
        resp = admin_session.post('/plots/create', data={
            'app': 'dna',
            'ptype': 'flot-line',
            'title': 'New Test Plot',
            'options': ''
        }, follow_redirects=False)
        assert resp.status_code == 302
        assert '/plots/edit' in resp.headers.get('Location', '')


class TestPlotInterface:
    """Tests for main plot interface route."""

    def test_plot_no_cid(self, guest_session):
        """GET /plot/<pltid> without cid returns error."""
        resp = guest_session.get('/plot/1?app=dna')
        assert resp.status_code == 200
        assert b'error' in resp.data.lower() or b'case id' in resp.data.lower()

    def test_plot_with_valid_case(self, guest_session, plot_case_with_data):
        """GET /plot/<pltid> with valid case shows plot."""
        cid = plot_case_with_data['cid']

        resp = guest_session.get(f'/plot/1?app=dna&cid={cid}')
        assert resp.status_code == 200

    def test_plot_with_pltid_zero(self, guest_session, plot_case_with_data):
        """GET /plot/0 finds first plot for app."""
        cid = plot_case_with_data['cid']

        resp = guest_session.get(f'/plot/0?app=dna&cid={cid}')
        assert resp.status_code == 200

    def test_plot_with_jid(self, guest_session, plot_case_with_data):
        """GET /plot/<pltid> accepts jid parameter."""
        cid = plot_case_with_data['cid']
        jid = plot_case_with_data['jid']

        resp = guest_session.get(f'/plot/1?app=dna&cid={cid}&jid={jid}')
        assert resp.status_code == 200

    def test_plot_shared_case(self, guest_session, admin_plot_case, admin_session):
        """User can view plot of shared case."""
        from spc.model import db, jobs

        cid = admin_plot_case['cid']

        # Make the case shared
        job = jobs(cid=cid)
        job.update_record(shared='True')
        db.commit()

        resp = guest_session.get(f'/plot/1?app=dna&cid=admin/{cid}')
        assert resp.status_code == 200

    def test_plot_unshared_case_forbidden(self, guest_session, app):
        """User cannot view plot of unshared case from other user."""
        from spc.model import db, jobs, users
        from spc.common import rand_cid
        from spc import user_data

        # Create an explicitly unshared case owned by admin
        uid = users(user='admin').id
        cid = rand_cid()

        jid = jobs.insert(
            uid=uid,
            app='dna',
            cid=cid,
            state='C',
            description='private plot case',
            time_submit=time.asctime(),
            walltime='3600',
            np=1,
            priority=3,
            shared='False'  # Explicitly set to False
        )
        db.commit()

        case_dir = os.path.join(user_data.user_data_root, 'admin', 'dna', cid)
        os.makedirs(case_dir, exist_ok=True)
        input_file = os.path.join(case_dir, 'dna.ini')
        with open(input_file, 'w') as f:
            f.write('[dna]\ndna=ATCG\n')
        din_file = os.path.join(case_dir, 'din.out')
        with open(din_file, 'w') as f:
            f.write('AA\t10\n')

        try:
            resp = guest_session.get(f'/plot/1?app=dna&cid=admin/{cid}')
            assert resp.status_code == 200
            assert b'forbidden' in resp.data.lower() or b'error' in resp.data.lower()
        finally:
            if os.path.exists(case_dir):
                shutil.rmtree(case_dir)
            parent = os.path.dirname(case_dir)
            if os.path.exists(parent) and not os.listdir(parent):
                os.rmdir(parent)
            if jobs(id=jid):
                del jobs[jid]
                db.commit()

    def test_plot_unsupported_type(self, guest_session, plot_case_with_data, admin_session):
        """GET /plot/<pltid> handles unsupported plot type."""
        from spc.model import db, plots as plots_table

        cid = plot_case_with_data['cid']

        # Create a plot with unsupported type
        pltid = plots_table.insert(appid=1, ptype='unsupported-type', title='Bad Plot', options='')
        db.commit()

        try:
            resp = guest_session.get(f'/plot/{pltid}?app=dna&cid={cid}')
            assert resp.status_code == 200
            assert b'not supported' in resp.data.lower() or b'error' in resp.data.lower()
        finally:
            del plots_table[pltid]
            db.commit()


class TestPlotTypes:
    """Tests for different plot types."""

    def test_flot_cat_plot(self, guest_session, plot_case_with_data):
        """GET /plot/<pltid> renders flot-cat plot."""
        cid = plot_case_with_data['cid']

        # Plot 1 is flot-cat type
        resp = guest_session.get(f'/plot/1?app=dna&cid={cid}')
        assert resp.status_code == 200

    def test_flot_scatter_plot(self, guest_session, plot_case_with_data, admin_session):
        """GET /plot/<pltid> renders flot-scatter plot."""
        from spc.model import db, plots as plots_table, datasource

        cid = plot_case_with_data['cid']

        # Create a scatter plot
        pltid = plots_table.insert(appid=1, ptype='flot-scatter', title='Scatter Plot', options='')
        db.commit()
        dsid = datasource.insert(pltid=pltid, label='Test', filename='data.dat', cols='1:2',
                                 line_range='', data_def='{label: "Test"}')
        db.commit()

        try:
            resp = guest_session.get(f'/plot/{pltid}?app=dna&cid={cid}')
            assert resp.status_code == 200
        finally:
            del datasource[dsid]
            del plots_table[pltid]
            db.commit()

    def test_plotly_hist_plot(self, guest_session, plot_case_with_data, admin_session):
        """GET /plot/<pltid> renders plotly-hist plot."""
        from spc.model import db, plots as plots_table, datasource

        cid = plot_case_with_data['cid']

        pltid = plots_table.insert(appid=1, ptype='plotly-hist', title='Histogram', options='')
        db.commit()
        dsid = datasource.insert(pltid=pltid, label='Test', filename='data.dat', cols='1',
                                 line_range='', data_def='')
        db.commit()

        try:
            resp = guest_session.get(f'/plot/{pltid}?app=dna&cid={cid}')
            assert resp.status_code == 200
        finally:
            del datasource[dsid]
            del plots_table[pltid]
            db.commit()

    def test_handson_plot(self, guest_session, plot_case_with_data, admin_session):
        """GET /plot/<pltid> renders handson (spreadsheet) plot."""
        from spc.model import db, plots as plots_table, datasource

        cid = plot_case_with_data['cid']

        pltid = plots_table.insert(appid=1, ptype='handson', title='Spreadsheet', options='')
        db.commit()
        dsid = datasource.insert(pltid=pltid, label='Test', filename='data.csv', cols='1:2',
                                 line_range='', data_def='')
        db.commit()

        try:
            resp = guest_session.get(f'/plot/{pltid}?app=dna&cid={cid}')
            assert resp.status_code == 200
        finally:
            del datasource[dsid]
            del plots_table[pltid]
            db.commit()


class TestPlotDataParsing:
    """Tests for plot data parsing edge cases."""

    def test_plot_with_line_range(self, guest_session, plot_case_with_data, admin_session):
        """Plot handles line_range parameter."""
        from spc.model import db, plots as plots_table, datasource

        cid = plot_case_with_data['cid']

        pltid = plots_table.insert(appid=1, ptype='flot-scatter', title='Range Plot', options='')
        db.commit()
        dsid = datasource.insert(pltid=pltid, label='Test', filename='data.dat', cols='1:2',
                                 line_range='1-20', data_def='{label: "Test"}')
        db.commit()

        try:
            resp = guest_session.get(f'/plot/{pltid}?app=dna&cid={cid}')
            assert resp.status_code == 200
        finally:
            del datasource[dsid]
            del plots_table[pltid]
            db.commit()

    def test_plot_with_single_column(self, guest_session, plot_case_with_data, admin_session):
        """Plot handles single column data."""
        from spc.model import db, plots as plots_table, datasource

        cid = plot_case_with_data['cid']

        pltid = plots_table.insert(appid=1, ptype='plotly-hist', title='Single Col', options='')
        db.commit()
        dsid = datasource.insert(pltid=pltid, label='Test', filename='data.dat', cols='2',
                                 line_range='', data_def='')
        db.commit()

        try:
            resp = guest_session.get(f'/plot/{pltid}?app=dna&cid={cid}')
            assert resp.status_code == 200
        finally:
            del datasource[dsid]
            del plots_table[pltid]
            db.commit()

    def test_plot_with_options(self, guest_session, plot_case_with_data, admin_session):
        """Plot handles options with tag replacement."""
        from spc.model import db, plots as plots_table, datasource

        cid = plot_case_with_data['cid']

        pltid = plots_table.insert(appid=1, ptype='flot-scatter', title='Options Plot',
                                   options='xaxis: {axisLabel: "X"}')
        db.commit()
        dsid = datasource.insert(pltid=pltid, label='Test', filename='data.dat', cols='1:2',
                                 line_range='', data_def='{label: "Test"}')
        db.commit()

        try:
            resp = guest_session.get(f'/plot/{pltid}?app=dna&cid={cid}')
            assert resp.status_code == 200
        finally:
            del datasource[dsid]
            del plots_table[pltid]
            db.commit()

    def test_plot_missing_data_file(self, guest_session, plot_case_with_data, admin_session):
        """Plot handles missing data file gracefully."""
        from spc.model import db, plots as plots_table, datasource

        cid = plot_case_with_data['cid']

        pltid = plots_table.insert(appid=1, ptype='flot-scatter', title='Missing File', options='')
        db.commit()
        dsid = datasource.insert(pltid=pltid, label='Test', filename='nonexistent.dat', cols='1:2',
                                 line_range='', data_def='{label: "Test"}')
        db.commit()

        try:
            resp = guest_session.get(f'/plot/{pltid}?app=dna&cid={cid}')
            assert resp.status_code == 200
            assert b'error' in resp.data.lower() or b'not found' in resp.data.lower()
        finally:
            del datasource[dsid]
            del plots_table[pltid]
            db.commit()


class TestMatplotlibRoute:
    """Tests for matplotlib plotting route."""

    @pytest.mark.skip(reason="Requires matplotlib which may not be installed")
    def test_matplotlib_plot(self, admin_session, admin_plot_case):
        """GET /mpl/<pltid> generates matplotlib plot."""
        cid = admin_plot_case['cid']

        # Note: This test requires matplotlib to be installed
        resp = admin_session.get(f'/mpl/1?app=dna&cid={cid}')
        assert resp.status_code == 200
