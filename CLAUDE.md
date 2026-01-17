# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SPC (Scientific Platform for the Cloud) is a Python 3 web platform for running parameterized scientific simulations. It provides a web UI for parameter entry, job scheduling, case management, file management, and result visualization (plotting).

**Tech Stack:** Flask + Jinja2 (web), pydal (SQLite data layer), boto3 (AWS), CherryPy (default server)

## Build & Development Commands

```bash
# Initialize (creates virtualenv, installs deps, initializes database)
./spc init

# Start the web server (default: http://localhost:8580)
./spc run

# Run tests with pytest (recommended)
./venv/bin/pytest tests/ -v

# Run a single test file
./venv/bin/pytest tests/test_login.py -v

# Run a single test
./venv/bin/pytest tests/test_login.py::TestLogin::test_login_valid_credentials -v

# Run legacy route tests (uses Flask test client internally)
./spc test

# Install an app from URL or local zip
./spc install /path/to/app.zip
./spc install https://url/to/app.zip

# Uninstall an app
./spc uninstall appname

# List installed apps
./spc list installed

# Migrate database schema changes
./spc migrate

# Build Sphinx docs
cd docs && make html
```

After `./spc init`, activate the virtualenv with `source venv/bin/activate` to run `spc` from anywhere.

## Architecture

### Core Structure
- `src/spc/` - Main application code
- `src/spc_apps/` - Installed scientific applications (symlinked as `apps/`)
- `src/spc/templates/` - Jinja2 templates (`.j2` files)
- `src/spc/static/` - Frontend assets (CSS, JS)
- `db/` - SQLite database files
- `user_data/` - Per-user simulation data organized as `user_data/<user>/<app>/<case_id>/`

### Key Modules
- `main.py` - Flask app setup, route registration, app loading
- `cli.py` - Command-line interface (`./spc` commands)
- `scheduler.py` - Multi-process job scheduler with queue states (Q=queued, R=running, C=completed, X=stopped)
- `app_reader_writer.py` - Input file format handlers (INI, XML, JSON, YAML, TOML, Namelist)
- `model.py` - Database schema (pydal): users, apps, jobs, plots, datasource, aws_creds
- `config.py` - Runtime configuration (auth, database, worker, server settings)

### Route Modules (Flask Blueprints)
Routes are registered via `register_routes()` in `main.py`. Each module has a `bind(globals)` function and `routes` blueprint:
- `account.py` - User registration, login, password management
- `admin.py` - Admin functions (user/app management)
- `app_routes.py` - App display, parameter confirmation, case management
- `execute.py` - Job submission and execution
- `jobs.py` - Job listing, status, stop/delete operations
- `plots.py` - Plot configuration and rendering
- `user_data.py` - File management, downloads
- `aws.py` - AWS integration
- `container.py` - Docker container support

### App Package Structure
Each app in `src/spc_apps/<appname>/` contains:
- `spc.json` - App metadata (name, description, command, input_format, plots)
- `<appname>` - Executable script
- `<appname>.<ext>` - Input template (`.ini`, `.xml`, `.json`, `.yaml`, `.toml`, or `.in` for namelist)
- `<appname>.j2` - Jinja2 template for the parameter input form

### Input Format Conventions
Apps use standardized input deck formats. The `app_reader_writer.py` module provides classes for each format that handle reading default parameters and writing user-submitted values:
- INI: `appname.ini`
- XML: `appname.xml`
- JSON: `appname.json`
- YAML: `appname.yaml`
- TOML: `appname.toml`
- Namelist: `appname.in` (Fortran-style)

### Job Execution Flow
1. User submits parameters via app form → `/confirm`
2. Parameters written to case directory: `user_data/<user>/<app>/<case_id>/`
3. Job queued via scheduler (`state='Q'`)
4. Scheduler polls, starts job process, redirects output to `<app>.out`
5. Job completes (`state='C'`) or times out (`state='X'`)

## Configuration

Edit `src/spc/config.py` to configure:
- `auth` - Enable/disable user authentication
- `server` - Web server (`cherrypy`, `uwsgi`, `wsgiref`)
- `port` - Listen port (default: 8580)
- `np` - Number of processors for job scheduler
- `worker` - Worker type (`local` or AWS)

## Testing

Tests are in `tests/` and use pytest with Flask's test client.

**Test structure:**
- `conftest.py` - Fixtures for test database, Flask client, and authenticated sessions
- `test_login.py` - Login, registration, password change routes
- `test_app_routes.py` - App display, parameter confirmation, execution
- `test_admin.py` - Admin routes, app configuration
- `test_scheduler.py` - Job scheduler unit tests
- `test_app_reader.py` - Input file format parsers (INI, JSON, YAML, Namelist)

**Key fixtures:**
- `client` - Unauthenticated Flask test client
- `guest_session` - Test client logged in as guest
- `admin_session` - Test client logged in as admin

## Style Guidelines

- 4-space indentation, no tabs
- `snake_case` for functions/variables, `CamelCase` for classes
- Templates use `.j2` extension (Jinja2)
- Keep changes consistent with surrounding code
