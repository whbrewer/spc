# Repository Guidelines

## Project Structure & Module Organization
SPC is a Python web platform with a Flask + Jinja2 stack. Key locations:
- `src/spc/`: core application (routes, scheduler, CLI, config).
- `src/spc_apps/`: installed scientific apps (symlinked as `apps/` at repo root).
- `src/spc/templates/`: Jinja2 `.j2` templates.
- `src/spc/static/`: frontend assets (CSS/JS/images).
- `tests/`: pytest suite and fixtures.
- `docs/`: Sphinx documentation.
- `db/`: SQLite database files created during init.
- `user_data/`: per-user app case data (`user_data/<user>/<app>/<case_id>/`).

## Build, Test, and Development Commands
Use the `./spc` CLI for most workflows:
- `./spc init`: create virtualenv, install deps, initialize database.
- `./spc run`: start the web server at `http://localhost:8580`.
- `./spc test`: run pytest suite.
- `./spc test --cov=src/spc`: run tests with coverage.
- `./spc test --legacy`: run legacy route tests.
- `./spc install <zip-or-url>` / `./spc uninstall <app>`: manage apps.
- `./spc list installed`: show installed apps.
- `./spc migrate`: apply database schema changes.
- `cd docs && make html`: build documentation.

## Coding Style & Naming Conventions
- Python uses 4-space indentation, no tabs.
- `snake_case` for functions/variables; `CamelCase` for classes.
- Templates use the `.j2` extension.
- No enforced formatter/linter; keep changes consistent with surrounding code.

## Testing Guidelines
- Framework: pytest with Flask test client.
- Tests live in `tests/` and follow `test_*.py` naming.
- Shared fixtures are in `tests/conftest.py` (e.g., `client`, `guest_session`).
- Run a single test: `./spc test tests/test_login.py::TestLogin::test_login_valid_credentials -v`.

## Commit & Pull Request Guidelines
- Commit messages in history are short, imperative, and capitalized.
  - Example: `Add pytest test suite`, `Fix screenshots`.
- PRs should include a clear description, linked issues (if any), and test results.
- Include screenshots for UI changes and note any config or schema impacts.

## Configuration & Data Notes
- Runtime settings live in `src/spc/config.py` (auth, server, port, worker).
- Do not commit generated `db/` or `user_data/` contents unless explicitly required.
