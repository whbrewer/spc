# SPC Release Notes

## 3/24/18

If you have any problems with using virtualenv, you may bypass using the virtualenv environment by simply running `python src/main.py run` from the main spc directory.

## 3/8/18

There are problems running spc with the Anaconda Python distribution (at least on Mac).  There seems to be some name collisions or something.  So, try using Mac's built-in Python instead.

## 8/29/17

If you want to run `./spc test` to test routes, need to first run `./spc requirements` on existing installation to update the 3rd party dependencies.

## 8/21/17

On some Amazon Linux systems, the "./spc requirements" command may install `psutil` in a lib64 directory, which will not be recognized by the path, and thereby not be imported.  This means that you won't get CPU and Memory stats showing up on the jobs monitor view.  This is discussed here: https://github.com/pypa/pip/issues/4464.  The fix is to reinstall psutil into venv/lib/python2.7/dist-packages using `pip --target` command line option.

## 8/14/17 

Since SPC v0.22, no longer can the app run command be specified or updated from the web interface. This was to prevent a major security vulnerability. Instead, edit the command field of the spc.json file for the app, and then run "./spc update appname command"

## 8/3/17 

Renamed {{title}} in app templates to {{tab_title}} because there was a name collision with the plot title.  All app templates need to be updated to reflect this change.

## 6/29/17 

SPC v0.20 has been restructured and uses auto dependency management via virtualenv.  To migrate older (pre-0.20 version) installations to this version:

1. Run `./spc requirements`
2. Move installed SPC apps to new location: `mv apps/* src/spc_apps` (then can remove `apps` directory)
3. Change the command in each app to look like: `<rel_apps_path>/appname/appname`.  This is easiest done by logging is as admin user and configure/edit the app.


## 2/19/17

Unfortunately I haven't found a good, robust way of handling database
migrations yet.  Gluino DAL has built-in migrations, but they don't
work always.  This is what is used when running "spc migrate".

The most recent git commit will modify the structure
of the datasource table to add a label column.  This was needed to
be able to properly support the "spc update" command.  To manually
fix this on older databases, use:

> alter table datasource add column label char(512);

at the sqlite3 command.  You may also have to run to turn on fake migrations by
editing src/migrate.py to have the parameter turn on as follows below.,

    self.db = DAL(uri, migrate=migrate, fake_migrate_all=True, folder=config.dbdir)

If you don't do this you may get an error the next time you run "spc migrate" or "spc update":
