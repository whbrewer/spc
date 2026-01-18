import sys, os, shutil, time, tempfile
import xml.etree.ElementTree as ET
import re, json, hashlib, zipfile
from urllib.request import urlopen

if os.path.exists("src/spc/config.py"):
    from . import config

sys.argv[1:]

url = 'https://s3-us-west-1.amazonaws.com/scihub'


def _convert_tpl_to_j2(src_path, dst_path):
    with open(src_path, 'r') as f:
        text = f.read()

    includes = re.compile(r"%\s*include\(([^)]+)\)")
    def _rewrite_include(match):
        raw = match.group(1).strip()
        if ',' in raw:
            raw = raw.split(',', 1)[0]
        raw = raw.strip().strip("'\"")
        if raw.endswith('.tpl'):
            raw = raw[:-4] + '.j2'
        elif not raw.endswith('.j2'):
            raw = raw + '.j2'
        return "{% include '" + raw + "' %}"

    has_rebase = False
    lines = []
    stack = []
    for line in text.splitlines():
        if re.search(r"%\s*rebase\(", line):
            has_rebase = True
            continue
        line = re.sub(r"^(\s*)%opts\s*=\s*(.+)$", r"\1{% set opts = \2 %}", line)
        line = includes.sub(_rewrite_include, line)
        line = re.sub(r"\{\{!\s*(.*?)\s*\}\}", r"{{ \1|safe }}", line)
        line = line.replace('opts.iteritems()', 'opts.items()')
        match = re.match(r'(\s*)%(if|for|elif|else|endif|endfor|end)\b', line.lstrip())
        if match:
            indent = line[:len(line) - len(line.lstrip())]
            tag = match.group(2)
            if tag in ('if', 'for'):
                stack.append(tag)
            elif tag == 'end':
                if stack:
                    last = stack.pop()
                    end_tag = '%endif' if last == 'if' else '%endfor'
                    line = indent + end_tag
        lines.append(line)

    body = "\n".join(lines).rstrip() + "\n"
    if has_rebase:
        body = "{% extends 'base.j2' %}\n{% block content %}\n" + body + "{% endblock %}\n"

    with open(dst_path, 'w') as f:
        f.write(body)

def usage():
    buf =  "usage: spc <command> [<args>]\n\n"
    buf += "available commands:\n\n"
    buf += "help          this output\n"
    buf += "import        import downloaded SPC case to local SPC instance\n"
    buf += "init          setup dependencies, database, and config.py file\n"
    buf += "install       install an app\n"
    buf += "list          list installed or available apps\n"
    buf += "migrate       migrate new database changes\n"
    buf += "requirements  install or update dependencies\n"
    buf += "run           start the server\n"
    buf += "runworker     start a worker\n"
    buf += "runsslworker  start an SSL worker\n"
    buf += "submit        submit a job (headless mode)\n"
    buf += "status        check job/case status\n"
    buf += "cases         list cases for an app\n"
    buf += "scheduler     run the job scheduler (headless)\n"
    buf += "shell         interactive REPL\n"
    buf += "test          run tests\n"
    buf += "uninstall     uninstall an app\n"
    # update is currently too buggy, don't release yet
    # buf += "update        update an app (in case spc.json was modified)\n"
    #buf += "search   search for available apps\n"
    return buf

if (len(sys.argv) == 1 or sys.argv[1] == "help"):
    print(usage())
    sys.exit()

#db = config.db

def create_config_file():
    """Create a config.py file in the spc directory"""
    fn="src/spc/config.py"
    if not os.path.exists(fn):
        with open(fn, "w") as f:
            f.write("# USER AUTHENTICATION\n")
            f.write("auth = False\n")
            f.write("\n# the number of rows to show at a time in the jobs table\n")
            f.write("jobs_num_rows = 20\n")
            f.write("\n# DATABASE\n")
            f.write("db = 'spc.db'\n")
            f.write("dbdir = 'db'\n")
            f.write("uri = 'sqlite://'+db\n")
            f.write("\n# DIRECTORIES\n")
            f.write("mpirun = '/usr/local/bin/mpirun'\n")
            f.write("default_priority = 3\n")
            f.write("# number of processors available to use on this machine\n")
            f.write("np = 1\n")
            f.write("\n# WORKERS\n")
            f.write("worker = 'local'\n")
            f.write("\n# WEB SERVER\n")
            f.write("# use 'wsgiref' for the Bottle built-in single-threaded dev server\n")
            f.write("# for a production system 'uwsgi' with NGINX is recommended\n")
            f.write("# 'cherrypy' is a decent multi-threaded server\n")
            f.write("# other options: 'rocket', 'bjoern', 'tornado', 'gae', etc.\n")
            f.write("server = 'cherrypy'\n")
            f.write("# port number to listen for connections\n")
            f.write("port = 8580\n")

def initdb():
    """Initializes database file"""
    from spc import config, migrate

    # create db directory if it doesn't exist
    if not os.path.exists(config.dbdir):
        os.makedirs(config.dbdir)

    # somehow the following doesn't work properly
    # make a backup copy of db file if it exists
    #if os.path.isfile(db):
    #    print "ERROR: a database file already exists, please rename it and rerun"
    #    sys.exit()
    #    shutil.copyfile(db, db+".bak")

    # get rid of old .table files
    for f in os.listdir(config.dbdir):
        if re.search(r"\.table", f):
            print("removing file:", f)
            os.remove(os.path.join(config.dbdir, f))
    # delete previous .db file should back first (future)
    dbpath = os.path.join(config.dbdir, config.db)
    if os.path.isfile(dbpath): os.remove(dbpath)
    # create db
    dal = migrate.dal(uri=config.uri, migrate=True)

    # add default groups
    admin_gid = dal.db.groups.insert(name="admin")
    guest_gid = dal.db.groups.insert(name="genetics")

    # add admin and guest user
    hashpw = hashlib.sha256("admin".encode('utf-8')).hexdigest()
    dal.db.users.insert(user="admin", passwd=hashpw, gid=admin_gid)
    hashpw = hashlib.sha256("guest".encode('utf-8')).hexdigest()
    dal.db.users.insert(user="guest", passwd=hashpw, gid=guest_gid)

    # add default app
    dal.db.apps.insert(name="dna",description="Compute reverse complement," +\
                       "GC content, and codon analysis of given DNA string.",
                       category="bioinformatics",
                       language="python",
                       input_format="ini",
                       command="<rel_apps_path>/dna/dna")
    dal.db.plots.insert(id=1, appid=1, ptype="flot-cat", title="Dinucleotides")
    dal.db.plots.insert(id=2, appid=1, ptype="flot-cat", title="Nucleotides")
    dal.db.plots.insert(id=3, appid=1, ptype="flot-cat", title="Codons")
    dal.db.datasource.insert(filename="din.out", cols="1:2", pltid=1, data_def='{label: "Dinucleotides"}')
    dal.db.datasource.insert(filename="nucs.out", cols="1:2", pltid=2, data_def='{label: "Nucleotides"}')
    dal.db.datasource.insert(filename="codons.out", cols="1:2", pltid=3, data_def='{label: "Codons"}')

    # activate the default app for admin and guest
    dal.db.app_user.insert(appid=1, uid=1)
    dal.db.app_user.insert(appid=1, uid=2)

    #dal.db.disciplines.insert(name="Chemistry")
    #dal.db.disciplines.insert(name="Linguistics")
    #dal.db.disciplines.insert(name="Finance")
    #dal.db.disciplines.insert(name="Biology")
    #dal.db.disciplines.insert(name="Physics")
    #dal.db.disciplines.insert(name="Fluid Dynamics")
    #dal.db.disciplines.insert(name="Geodynamics")
    #dal.db.disciplines.insert(name="Molecular Dynamics")
    #dal.db.disciplines.insert(name="Weather Prediction")
    # write changes to db
    dal.db.commit()

def migrate():
    """Migrate DB schema changes"""
    from spc import migrate
    dal = migrate.dal(uri=config.uri, migrate=True)

    # add default groups
    dal.db.groups.update_or_insert(name="admin")
    dal.db.groups.update_or_insert(name="default")

    # need to run:
    # alter table datasource add column label text;

    # need to get this working in the future
    # default = 1
    # update all group ids to be 1 for now
    # dal.db.jobs(dal.db.jobs.id > 0).update_record(gid=default)
    # dal.db.apps(dal.db.apps.id > 0).update_record(gid=default)
    # dal.db.users(dal.db.users.id > 0).update_record(gid=default)

    dal.db.commit()

notyet = "this feature not yet working"

# ref: http://stackoverflow.com/questions/4028697
def dlfile(url):
    # Open the url
    try:
        f = urlopen(url)
        print("downloading " + url)
        # Open our local file for writing
        with open(os.path.basename(url), "wb") as local_file:
            local_file.write(f.read())
    #handle errors
    except HTTPError as e:
        print("HTTP Error:", e.code, url)
    except URLError as e:
        print("URL Error:", e.reason, url)

# process command line options
def main():
    if (sys.argv[1] == "init"):
        create_config_file()
        print("creating database.")
        initdb()
    elif (sys.argv[1] == "migrate"):
        print("migrating database schema changes")
        migrate()
    elif (sys.argv[1] == "run"):
        from . import config
        if config.server == 'uwsgi':
            os.system('/usr/local/bin/uwsgi etc/uwsgi.ini')
        else:
            import spc.main
            spc.main.main()
    elif (sys.argv[1] == "runworker"):
        import spc.worker
        spc.worker.main()
    elif (sys.argv[1] == "runsslworker"):
        import spc.worker_ssl
        spc.worker_ssl.main()
    elif (sys.argv[1] == "search"):
        print(notyet)
    elif (sys.argv[1] == "test"):
        # Run pytest by default, or legacy tests with --legacy flag
        if len(sys.argv) > 2 and sys.argv[2] == "--legacy":
            import spc.test
            spc.test.main()
        else:
            # Run pytest test suite
            import subprocess
            repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            pytest_path = os.path.join(repo_root, 'venv', 'bin', 'pytest')
            tests_path = os.path.join(repo_root, 'tests')

            if not os.path.exists(pytest_path):
                print("ERROR: pytest not found. Run './spc init' first.")
                sys.exit(1)

            # Pass any additional arguments to pytest (e.g., -v, --cov)
            extra_args = sys.argv[2:] if len(sys.argv) > 2 else ['-v']
            cmd = [pytest_path, tests_path] + extra_args
            sys.exit(subprocess.call(cmd))

    elif sys.argv[1] == "submit":
        # Headless job submission
        # Usage: spc submit <app> [--params "key=val,key2=val2"] [--desc "description"] [--np N]
        from . import migrate, config
        from . import app_reader_writer as apprw
        from .common import rand_cid, replace_tags

        submit_usage = """usage: spc submit <app> [options]

options:
  --params "key=val,key2=val2"   parameters to pass to the app
  --desc "description"           job description
  --np N                         number of processors (default: 1)
  --user USERNAME                username (default: cli)

examples:
  spc submit dna --params "dna=ATCGATCG"
  spc submit mendel --params "pop_size=1000,generations=500" --desc "test run"
"""
        if len(sys.argv) < 3:
            print(submit_usage)
            sys.exit(1)

        app_name = sys.argv[2]

        # Parse optional arguments
        params_str = ""
        desc = ""
        np = 1
        user = "cli"

        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--params" and i + 1 < len(sys.argv):
                params_str = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--desc" and i + 1 < len(sys.argv):
                desc = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--np" and i + 1 < len(sys.argv):
                np = int(sys.argv[i + 1])
                i += 2
            elif sys.argv[i] == "--user" and i + 1 < len(sys.argv):
                user = sys.argv[i + 1]
                i += 2
            else:
                print(f"Unknown option: {sys.argv[i]}")
                print(submit_usage)
                sys.exit(1)

        # Connect to database
        dal = migrate.dal(uri=config.uri)
        db = dal.db

        # Check if app exists
        app_row = db(db.apps.name == app_name).select().first()
        if not app_row:
            print(f"ERROR: app '{app_name}' not found. Use 'spc list installed' to see available apps.")
            sys.exit(1)

        # Get or create user
        user_row = db(db.users.user == user).select().first()
        if not user_row:
            # Create CLI user with default priority
            uid = db.users.insert(user=user, passwd="", priority=3)
            db.commit()
        else:
            uid = user_row.id

        # Generate case ID
        cid = rand_cid()

        # Parse parameters (seed with app defaults so missing fields aren't "F")
        params = dict(myapp.params) if getattr(myapp, "params", None) else {}
        params.update({'case_id': cid, 'cid': cid, 'user': user})
        if params_str:
            for pair in params_str.split(','):
                if '=' in pair:
                    key, val = pair.split('=', 1)
                    params[key.strip()] = val.strip()

        # Create app instance and write parameters
        input_format = app_row.input_format or 'ini'
        if input_format == 'namelist':
            myapp = apprw.Namelist(app_name)
        elif input_format == 'ini':
            myapp = apprw.INI(app_name)
        elif input_format == 'json':
            myapp = apprw.JSON(app_name)
        elif input_format == 'yaml':
            myapp = apprw.YAML(app_name)
        elif input_format == 'toml':
            myapp = apprw.TOML(app_name)
        elif input_format == 'xml':
            myapp = apprw.XML(app_name)
        else:
            myapp = apprw.INI(app_name)

        # Write parameters to case directory
        myapp.write_params(params, user)

        # Build command
        cmd = app_row.command or f"./{app_name}"
        params['rel_apps_path'] = (os.pardir + os.sep) * 4 + apprw.apps_dir
        cmd = replace_tags(cmd, params)

        # Submit job to database
        priority = user_row.priority if user_row else 3
        jid = db.jobs.insert(
            uid=uid,
            app=app_name,
            cid=cid,
            command=cmd,  # Store the command
            state='Q',
            description=desc,
            time_submit=time.strftime("%a %b %d %H:%M:%S %Y"),
            walltime=3600,
            np=np,
            priority=priority
        )
        db.commit()

        print(f"Job submitted successfully!")
        print(f"  Case ID: {cid}")
        print(f"  Job ID:  {jid}")
        print(f"  App:     {app_name}")
        print(f"  Status:  Queued")
        print(f"\nTo check status: spc status {cid}")
        print(f"To start scheduler and run jobs: spc run")

    elif sys.argv[1] == "status":
        # Check job/case status
        # Usage: spc status <cid>
        from . import migrate, config

        if len(sys.argv) < 3:
            print("usage: spc status <case_id>")
            sys.exit(1)

        cid = sys.argv[2]

        dal = migrate.dal(uri=config.uri)
        db = dal.db

        job = db(db.jobs.cid == cid).select().first()
        if not job:
            print(f"ERROR: case '{cid}' not found")
            sys.exit(1)

        # Get user name
        user_row = db(db.users.id == job.uid).select().first()
        username = user_row.user if user_row else "unknown"

        # State descriptions
        states = {
            'Q': 'Queued',
            'R': 'Running',
            'C': 'Completed',
            'X': 'Stopped/Failed'
        }
        state_desc = states.get(job.state, job.state)

        print(f"Case: {cid}")
        print(f"  Job ID:      {job.id}")
        print(f"  App:         {job.app}")
        print(f"  User:        {username}")
        print(f"  Status:      {state_desc}")
        print(f"  Description: {job.description or '(none)'}")
        print(f"  Submitted:   {job.time_submit}")
        print(f"  Processors:  {job.np}")

        # Show output file location
        user_data_dir = os.path.join('user_data', username, job.app, cid)
        if os.path.isdir(user_data_dir):
            print(f"  Output dir:  {user_data_dir}")
            out_file = os.path.join(user_data_dir, f"{job.app}.out")
            if os.path.isfile(out_file):
                # Show last few lines of output
                print(f"\nLast 5 lines of output:")
                with open(out_file, 'r') as f:
                    lines = f.readlines()
                    for line in lines[-5:]:
                        print(f"  {line.rstrip()}")

    elif sys.argv[1] == "cases":
        # List cases for an app
        # Usage: spc cases [app] [--user USERNAME] [--state STATE]
        from . import migrate, config

        cases_usage = """usage: spc cases [app] [options]

options:
  --user USERNAME    filter by user (default: all)
  --state STATE      filter by state: Q, R, C, X (default: all)
  --limit N          max number of cases to show (default: 20)

examples:
  spc cases                    # list all recent cases
  spc cases dna                # list cases for dna app
  spc cases --state R          # list running jobs
  spc cases mendel --user cli  # list mendel cases for cli user
"""
        app_filter = None
        user_filter = None
        state_filter = None
        limit = 20

        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--user" and i + 1 < len(sys.argv):
                user_filter = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--state" and i + 1 < len(sys.argv):
                state_filter = sys.argv[i + 1].upper()
                i += 2
            elif sys.argv[i] == "--limit" and i + 1 < len(sys.argv):
                limit = int(sys.argv[i + 1])
                i += 2
            elif sys.argv[i] == "--help":
                print(cases_usage)
                sys.exit(0)
            elif not sys.argv[i].startswith("--"):
                app_filter = sys.argv[i]
                i += 1
            else:
                print(f"Unknown option: {sys.argv[i]}")
                print(cases_usage)
                sys.exit(1)

        dal = migrate.dal(uri=config.uri)
        db = dal.db

        # Build query
        query = db.jobs.id > 0
        if app_filter:
            query &= db.jobs.app == app_filter
        if state_filter:
            query &= db.jobs.state == state_filter
        if user_filter:
            user_row = db(db.users.user == user_filter).select().first()
            if user_row:
                query &= db.jobs.uid == user_row.id
            else:
                print(f"No cases found for user '{user_filter}'")
                sys.exit(0)

        jobs = db(query).select(orderby=~db.jobs.id, limitby=(0, limit))

        if not jobs:
            print("No cases found")
            sys.exit(0)

        # State descriptions
        states = {'Q': 'Queued', 'R': 'Running', 'C': 'Done', 'X': 'Failed'}

        # Print header
        print(f"{'CID':<10} {'APP':<12} {'STATUS':<10} {'USER':<10} {'DESCRIPTION':<30}")
        print("-" * 75)

        for job in jobs:
            user_row = db(db.users.id == job.uid).select().first()
            username = user_row.user if user_row else "?"
            state_desc = states.get(job.state, job.state)
            desc = (job.description or "")[:28]
            print(f"{job.cid:<10} {job.app:<12} {state_desc:<10} {username:<10} {desc:<30}")

        print(f"\nShowing {len(jobs)} case(s)")

    elif sys.argv[1] == "scheduler":
        # Run the scheduler without the web server
        from . import config
        from .scheduler import Scheduler

        print("Starting SPC scheduler (headless mode)...")
        print(f"  Max concurrent jobs: {config.np}")
        print("  Press Ctrl+C to stop\n")

        sched = Scheduler()
        sched.poll()

        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nScheduler stopped.")

    elif sys.argv[1] == "shell":
        # Interactive REPL
        from . import migrate, config
        from . import app_reader_writer as apprw
        from .common import rand_cid, replace_tags
        from .scheduler import Scheduler

        print("SPC Interactive Shell")
        print("Type 'help' for available commands, 'quit' to exit\n")

        dal = migrate.dal(uri=config.uri)
        db = dal.db
        sched = None

        def show_help():
            print("""
Available commands:
  apps                          list installed apps
  submit <app> [params]         submit a job (params: key=val,key2=val2)
  status [cid]                  show job status (or all if no cid)
  cases [app]                   list cases
  start                         start the scheduler
  stop                          stop the scheduler
  tail <cid>                    show output of a case
  help                          show this help
  quit                          exit the shell
""")

        def list_apps():
            rows = db(db.apps.id > 0).select()
            if not rows:
                print("No apps installed")
                return
            print(f"{'NAME':<15} {'FORMAT':<10} {'DESCRIPTION':<40}")
            print("-" * 65)
            for row in rows:
                desc = (row.description or "")[:38]
                print(f"{row.name:<15} {row.input_format or 'ini':<10} {desc:<40}")

        def submit_job(args):
            if not args:
                print("Usage: submit <app> [key=val,key2=val2]")
                return

            parts = args.split(None, 1)
            app_name = parts[0]
            params_str = parts[1] if len(parts) > 1 else ""
            if params_str.startswith("--params"):
                params_str = params_str[len("--params"):].lstrip()
            if (params_str.startswith('"') and params_str.endswith('"')) or (
                params_str.startswith("'") and params_str.endswith("'")
            ):
                params_str = params_str[1:-1]

            app_row = db(db.apps.name == app_name).select().first()
            if not app_row:
                print(f"App '{app_name}' not found")
                return

            # Get or create CLI user
            user = "cli"
            user_row = db(db.users.user == user).select().first()
            if not user_row:
                uid = db.users.insert(user=user, passwd="", priority=3)
                db.commit()
                user_row = db(db.users.id == uid).select().first()
            uid = user_row.id

            # Create app instance
            input_format = app_row.input_format or 'ini'
            app_classes = {
                'namelist': apprw.Namelist,
                'ini': apprw.INI,
                'json': apprw.JSON,
                'yaml': apprw.YAML,
                'toml': apprw.TOML,
                'xml': apprw.XML
            }
            myapp = app_classes.get(input_format, apprw.INI)(app_name)
            cid = rand_cid()
            params = dict(myapp.params) if getattr(myapp, "params", None) else {}
            params.update({'case_id': cid, 'cid': cid, 'user': user})
            if params_str:
                for pair in params_str.split(','):
                    if '=' in pair:
                        key, val = pair.split('=', 1)
                        params[key.strip()] = val.strip()
            myapp.write_params(params, user)

            # Build command
            cmd = app_row.command or f"./{app_name}"
            params['rel_apps_path'] = (os.pardir + os.sep) * 4 + apprw.apps_dir
            cmd = replace_tags(cmd, params)

            # Submit job
            jid = db.jobs.insert(
                uid=uid,
                app=app_name,
                cid=cid,
                command=cmd,  # Store the command
                state='Q',
                description="",
                time_submit=time.strftime("%a %b %d %H:%M:%S %Y"),
                walltime=3600,
                np=1,
                priority=user_row.priority or 3
            )
            db.commit()
            print(f"Submitted: cid={cid} jid={jid}")

        def show_status(cid=None):
            states = {'Q': 'Queued', 'R': 'Running', 'C': 'Done', 'X': 'Failed'}
            if cid:
                job = db(db.jobs.cid == cid).select().first()
                if not job:
                    print(f"Case '{cid}' not found")
                    return
                user_row = db(db.users.id == job.uid).select().first()
                print(f"Case {cid}: {states.get(job.state, job.state)} ({job.app})")
            else:
                jobs = db(db.jobs.id > 0).select(orderby=~db.jobs.id, limitby=(0, 10))
                if not jobs:
                    print("No jobs")
                    return
                print(f"{'CID':<10} {'APP':<10} {'STATUS':<10}")
                print("-" * 32)
                for job in jobs:
                    print(f"{job.cid:<10} {job.app:<10} {states.get(job.state, job.state):<10}")

        def list_cases(app_filter=None):
            query = db.jobs.id > 0
            if app_filter:
                query &= db.jobs.app == app_filter
            jobs = db(query).select(orderby=~db.jobs.id, limitby=(0, 20))
            states = {'Q': 'Queued', 'R': 'Running', 'C': 'Done', 'X': 'Failed'}
            if not jobs:
                print("No cases")
                return
            print(f"{'CID':<10} {'APP':<12} {'STATUS':<10} {'DESCRIPTION':<30}")
            print("-" * 65)
            for job in jobs:
                desc = (job.description or "")[:28]
                print(f"{job.cid:<10} {job.app:<12} {states.get(job.state, job.state):<10} {desc:<30}")

        def start_scheduler():
            nonlocal sched
            if sched:
                print("Scheduler already running")
                return
            sched = Scheduler()
            sched.poll()
            print("Scheduler started")

        def stop_scheduler():
            nonlocal sched
            if not sched:
                print("Scheduler not running")
                return
            sched = None
            print("Scheduler stopped (running jobs will complete)")

        def tail_output(cid):
            job = db(db.jobs.cid == cid).select().first()
            if not job:
                print(f"Case '{cid}' not found")
                return
            user_row = db(db.users.id == job.uid).select().first()
            username = user_row.user if user_row else "unknown"
            out_file = os.path.join('user_data', username, job.app, cid, f"{job.app}.out")
            if os.path.isfile(out_file):
                with open(out_file, 'r') as f:
                    lines = f.readlines()
                    for line in lines[-20:]:
                        print(line.rstrip())
            else:
                print(f"No output file yet: {out_file}")

        # REPL loop
        while True:
            try:
                line = input("spc> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break

            if not line:
                continue

            parts = line.split(None, 1)
            cmd = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            if cmd in ('quit', 'exit', 'q'):
                print("Goodbye!")
                break
            elif cmd == 'help':
                show_help()
            elif cmd == 'apps':
                list_apps()
            elif cmd == 'submit':
                submit_job(args)
            elif cmd == 'status':
                show_status(args if args else None)
            elif cmd == 'cases':
                list_cases(args if args else None)
            elif cmd == 'start':
                start_scheduler()
            elif cmd == 'stop':
                stop_scheduler()
            elif cmd == 'tail':
                if args:
                    tail_output(args)
                else:
                    print("Usage: tail <cid>")
            else:
                print(f"Unknown command: {cmd}. Type 'help' for available commands.")

    elif (sys.argv[1] == "uninstall"):
        from . import app_reader_writer as apprw
        install_usage = "usage: spc uninstall appname"
        if len(sys.argv) == 3:
            from . import migrate, config

            app = sys.argv[2]
            a = apprw.App(app)
            # connect to db
            dal = migrate.dal(uri=config.uri)
            result = dal.db(dal.db.apps.name==app).select()
            if result:
                appid = dal.db(dal.db.apps.name==app).select().first()["id"]
                # delete associated data
                dal.db(dal.db.app_user.appid == appid).delete()
                plot_rows = dal.db(dal.db.plots.appid == appid).select(dal.db.plots.id)
                for row in plot_rows:
                    dal.db(dal.db.datasource.pltid == row.id).delete()
                dal.db(dal.db.plots.appid == appid).delete()
                dal.db(dal.db.apps.id == appid).delete()
                dal.db.commit()

                # delete app directory, template, and static assets
                app_path = os.path.join(apprw.apps_dir, app)
                if os.path.isdir(app_path):
                    shutil.rmtree(app_path)
                tpl_path = os.path.join('src', 'spc', 'templates', 'apps', app + '.j2')
                if os.path.isfile(tpl_path):
                    os.remove(tpl_path)
                tpl_legacy = os.path.join('src', 'spc', 'templates', 'apps', app + '.tpl')
                if os.path.isfile(tpl_legacy):
                    os.remove(tpl_legacy)
                static_path = os.path.join('static', 'apps', app)
                if os.path.isdir(static_path):
                    shutil.rmtree(static_path)

                print("SUCCESS: uninstalled app", app, "with appid:", appid)
            else:
                print("ERROR: app does not exist")
                sys.exit()
        else:
            print(install_usage)

    elif (sys.argv[1] == "import"):
        if len(sys.argv) <= 2:
            print("usage: spc import zipcase.zip (file.zip downloaded from another SPC instance)")
            sys.exit()
        else:
            save_path = sys.argv[2]

        filename, file_extension = os.path.splitext(save_path)

        if file_extension == ".zip":

            print("importing zip file:", save_path)

            # unzip file
            fh = open(save_path, 'rb')
            z = zipfile.ZipFile(fh)
            z.extractall()
            # depending on how file was zipped, the extracted directory
            # may be different than the zip filename, so update the app_dir_name
            # to the extracted filename
            app_dir_name = z.namelist()[0]
            fh.close()

            # get the username, appname, and case id out of the file structure
            _, user, app, cid, _ = z.namelist()[0].split(os.sep)

            # delete zip file
            user_input = input('Remove zip file? [Yn] ') or 'y'
            if user_input.lower() == 'y':
                os.unlink(save_path)
                print("removed zip file", save_path)
            else:
                print("file not removed")

        else:
            print("importing directory:", save_path)
            _, user, app, cid = save_path.split(os.sep)

        # add case to database
        from . import migrate, config
        dal = migrate.dal(uri=config.uri, migrate=True)
        uid = dal.db.users(user=user).id
        dal.db.jobs.insert(uid=uid, app=app, cid=cid, state="D",
                       description="", time_submit=time.asctime(),
                       walltime="", np="", priority="")
        dal.db.commit()

        print("imported case. user:", user, "app:", app, "cid:", cid)

    elif (sys.argv[1] == "install"):
        from . import app_reader_writer as apprw
        #import platform
        #platform.system()  # Darwin, Linux, Windows, or Java
        #platform.machine() # i386, x86_64
        install_usage = "usage: spc install /path/to/file.zip\n    or spc install http://url/to/file.zip"

        if len(sys.argv) == 3:
            from . import migrate, config

            if re.search(r'http[s]://.*$', sys.argv[2]):
                dlfile(sys.argv[2]) # download zip file
                # if url is http://website.com/path/to/file.zip
                # following line extracts out just "file.zip" which should
                # now be in the current directory
                save_path = os.path.basename(sys.argv[2].split('//')[1])
            else:
                save_path = sys.argv[2]

            # unzip file into a temp directory to avoid cluttering cwd
            extract_dir = tempfile.mkdtemp(prefix="spc-install-")
            with zipfile.ZipFile(save_path) as z:
                z.extractall(extract_dir)

            # delete downloaded zip file
            if re.search(r'http[s]://.*$', sys.argv[2]):
                os.unlink(save_path)

            # delete __MACOSX dir if exists
            macosx_dir = os.path.join(extract_dir, "__MACOSX")
            if os.path.exists(macosx_dir):
                shutil.rmtree(macosx_dir)

            # locate spc.json (support flat or nested archives)
            app_root = None
            if os.path.isfile(os.path.join(extract_dir, "spc.json")):
                app_root = extract_dir
            else:
                for root, _, files in os.walk(extract_dir):
                    if "spc.json" in files:
                        app_root = root
                        break

            if not app_root:
                shutil.rmtree(extract_dir)
                print('ERROR: spc.json not found in archive')
                sys.exit()

            # read the json app config file and insert info into db
            path = os.path.join(app_root, "spc.json")
            with open(path,'r') as f:
                data = f.read()
            parsed = json.loads(data)

            # get name of app from json data
            app = parsed['name']
            app_path = apprw.apps_dir + os.sep + app

            if os.path.exists(app_path):
                print('ERROR: app directory exists already. Please remove first.')
                shutil.rmtree(extract_dir)
                sys.exit()

            # move app files to apps folder
            if app_root == extract_dir:
                os.makedirs(app_path)
                for name in os.listdir(extract_dir):
                    shutil.move(os.path.join(extract_dir, name), app_path)
                shutil.rmtree(extract_dir)
            else:
                shutil.move(app_root, app_path)
                shutil.rmtree(extract_dir)

            # connect to db
            dal = migrate.dal(uri=config.uri)

            # check if app already exists before preceding
            result = dal.db(dal.db.apps.name==parsed['name']).select().first()
            if result:
                print("\n*** ERROR: app already exists in database ***")
                shutil.rmtree(app_path)
                sys.exit()

            # copy or convert template file to templates/apps folder
            app_template_dir = apprw.apps_dir + os.sep + app
            src = os.path.join(app_template_dir, app + '.j2')
            if not os.path.exists(src):
                tpl_src = os.path.join(app_template_dir, app + '.tpl')
                if os.path.exists(tpl_src):
                    _convert_tpl_to_j2(tpl_src, src)
                else:
                    raise RuntimeError("Missing app template: {}".format(src))
            dst = os.path.join('src', 'spc', 'templates', 'apps')
            if not os.path.exists(dst):
                os.makedirs(dst)
            shutil.copy(src, dst)

            # turn on executable bit
            path = os.path.join(apprw.apps_dir, app, app)
            if os.path.exists(path): os.chmod(path, 0o700)

            # add app to database
            appid = dal.db.apps.insert(name=app,
                               description=parsed['description'],
                               category=parsed['category'],
                               language=parsed['language'],
                               input_format=parsed['input_format'],
                               command=parsed['command'],
                               assets=', '.join(parsed['assets']),
                               preprocess=parsed['preprocess'],
                               postprocess=parsed['postprocess'])

            # copy static assets to src/spc/static/apps/appname directory
            stat_apps_dir = os.path.join('src', 'spc', 'static', 'apps')
            if not os.path.exists(stat_apps_dir):
                os.makedirs(stat_apps_dir)

            stat_app_dir = os.path.join(stat_apps_dir, app)
            if not os.path.exists(stat_app_dir):
                os.makedirs(stat_app_dir)

            dst = os.path.join('src', 'spc', 'static', 'apps', app)
            if 'assets' in parsed.keys():
                for asset in parsed['assets']:
                    src = os.path.join(apprw.apps_dir, app, asset)
                    shutil.copy(src, dst)

            # add plots and datasources to db
            if 'plots' in parsed.keys():
                for key in parsed['plots']:
                    if key['ptype'] == 'flot-3d':
                        # For flot-3d we need different fields than other plot types
                        # so as a hack we json encode everything and save it in
                        # the filename field
                        pltid = dal.db.plots.insert(
                            appid=appid,
                            ptype=key['ptype'],
                            title=key['title'],
                            options=json.dumps(key['options'])
                        )
                    else:
                        pltid = dal.db.plots.insert(
                            appid=appid,
                            ptype=key['ptype'],
                            title=key['title'],
                            options=key['options']
                        )

                        for ds in key['datasource']:
                            dal.db.datasource.insert(pltid=pltid,
                                                     filename=ds['filename'],
                                                     cols=ds['cols'],
                                                     line_range=ds['line_range'],
                                                     data_def=ds['data_def'])

            # commit to db
            dal.db.commit()
            print("SUCCESS: installed app", app)
            print("Note: If SPC is running, you will need to restart")
        else:
            print(install_usage)

    elif (sys.argv[1] == "list"):
        from spc import config
        list_usage = "usage: spc list [available|installed]"
        if (len(sys.argv) == 3):
            if (sys.argv[2] == "installed"):
                from spc import migrate
                dal = migrate.dal(uri=config.uri)
                result = dal.db().select(dal.db.apps.ALL)
                for r in result: print(r.name)
            elif (sys.argv[2] == "available"):
                try:
                    response = urlopen(url)
                    html = response.read()
                    root = ET.fromstring(html)
                    for child in root.findall("{http://s3.amazonaws.com/doc/2006-03-01/}Contents"):
                        for c in child.findall("{http://s3.amazonaws.com/doc/2006-03-01/}Key"):
                            (app, ext) = c.text.split(".")
                            print(app)
                except:
                    print("ERROR: problem accessing network")
                    sys.exit()
            else:
                print(list_usage)
        else:
            print(list_usage)

    elif (sys.argv[1] == "update"):
        from . import migrate, config, app_reader_writer as apprw

        usage = "usage: spc update appname [command|plots]"

        if len(sys.argv) > 2:
            app = sys.argv[2]
        else:
            print(usage)
            sys.exit()

        app_path = apprw.apps_dir + os.sep + app
        dal = migrate.dal(uri=config.uri, migrate=True)

        # check if directory exists
        if not os.path.isdir(app_path):
            print('ERROR: app directory does not exist')
            print(usage)
            sys.exit()

        file_path = os.path.join(app_path, "spc.json")

        if not os.path.isfile(os.path.join(app_path, "spc.json")):
            print('ERROR: spc.json file does not exist in ' + app_path)
            sys.exit()

        # read the json app config file and insert info into db
        with open(file_path,'r') as f:
            data = f.read()
        parsed = json.loads(data)

        # check if this is the correct spc.json for the app specified
        if not app == parsed['name']:
            print('ERROR: app name specified in spc.json file different than command line')
            sys.exit()
        else:
            appid = dal.db.apps(name=app).id

        if len(sys.argv) == 4:

            if sys.argv[3] == "command":
                dal = migrate.dal(uri=config.uri, migrate=True)
                dal.db.apps(name=sys.argv[2]).update_record(command=parsed['command'])
                dal.db.commit()
                print("updated", app, "command to:", parsed['command'])

            elif sys.argv[3] == "plots":

                np = nd = 0
                # update plots and datasources
                if 'plots' in parsed.keys():

                    for key in parsed['plots']:
                        sys.stdout.write('P')
                        # following is not working but it should be the proper way to implement
                        nrecords = dal.db.plots.update_or_insert(dal.db.plots.title==key['title'],
                                                                 appid=appid, ptype=key['ptype'],
                                                                 title=key['title'], options=key['options'])

                        if nrecords is not None:
                            print('\nINFO: inserting plot definition', key['title'])
                            np += 1

                        pltid = dal.db.plots(title=key['title']).id

                        for ds in key['datasource']:
                            sys.stdout.write('.')
                            nrecords = dal.db.datasource.update_or_insert(
                                                     dal.db.datasource.label==ds['label'],
                                                     label=ds['label'], pltid=pltid,
                                                     filename=ds['filename'],
                                                     cols=ds['cols'],
                                                     line_range=ds['line_range'],
                                                     data_def=ds['data_def'])
                            if nrecords is not None:
                                print('\nINFO: inserting datasource for plt', pltid)
                                nd += 1

                # commit changes to db
                dal.db.commit()
                print()
                if np > 0: print("SUCCESS: inserted", np, "plot defs")
                if nd > 0: print("SUCCESS: inserted defs for app", app)
                print()
                print("NOTE: some plot records may have been updated but currently web2py DAL does not notify about that")
            else:
                print("ERROR: option not supported")
                sys.exit()
        else:
            print(usage)
            sys.exit()

    elif sys.argv[1] == "requirements":
        os.system('virtualenv venv')
        os.system('./venv/bin/pip install -r requirements.txt')
    else:
        print("ERROR: option not supported")
        sys.exit()
