import builtins
import importlib
import re
import sys

import pytest


def _set_user_data_root(monkeypatch, tmp_path):
    root = tmp_path / "user_data"
    root.mkdir()
    from spc import user_data
    from spc import app_reader_writer as apprw
    monkeypatch.setattr(user_data, "user_data_root", str(root))
    monkeypatch.setattr(apprw, "user_data_root", str(root))
    return root


def _run_cli(monkeypatch, argv, pre_main=None):
    monkeypatch.setattr(sys, "argv", argv)
    import spc.cli as cli
    importlib.reload(cli)
    if pre_main:
        pre_main(cli)
    cli.main()


def _run_cli_expect_exit(monkeypatch, argv, pre_main=None):
    monkeypatch.setattr(sys, "argv", argv)
    import spc.cli as cli
    importlib.reload(cli)
    if pre_main:
        pre_main(cli)
    with pytest.raises(SystemExit):
        cli.main()


def test_headless_submit_and_status(app, monkeypatch, tmp_path, capsys):
    _set_user_data_root(monkeypatch, tmp_path)

    _run_cli(monkeypatch, ["spc", "submit", "dna", "--params", "dna=ATCG", "--desc", "test run"])
    out = capsys.readouterr().out
    match = re.search(r"Case ID:\s+(\w+)", out)
    assert match, out
    cid = match.group(1)

    from spc import migrate, config
    dal = migrate.dal(uri=config.uri)
    job = dal.db(dal.db.jobs.cid == cid).select().first()
    assert job is not None
    assert job.state == "Q"

    ini_path = tmp_path / "user_data" / "cli" / "dna" / cid / "dna.ini"
    assert ini_path.exists()

    _run_cli(monkeypatch, ["spc", "status", cid])
    status_out = capsys.readouterr().out
    assert "Status:" in status_out
    assert "Queued" in status_out


def test_shell_basic_commands(app, monkeypatch, tmp_path, capsys):
    _set_user_data_root(monkeypatch, tmp_path)

    commands = iter([
        "apps",
        "submit dna dna=ATCG",
        "status",
        "quit",
    ])

    def fake_input(_prompt=""):
        return next(commands)

    monkeypatch.setattr(builtins, "input", fake_input)

    _run_cli(monkeypatch, ["spc", "shell"])
    out = capsys.readouterr().out
    assert "SPC Interactive Shell" in out
    assert "Submitted: cid=" in out
    assert "STATUS" in out


def test_submit_usage_and_unknown_option(app, monkeypatch, tmp_path, capsys):
    _set_user_data_root(monkeypatch, tmp_path)

    _run_cli_expect_exit(monkeypatch, ["spc", "submit"])
    out = capsys.readouterr().out
    assert "usage: spc submit" in out

    _run_cli_expect_exit(monkeypatch, ["spc", "submit", "dna", "--nope"])
    out = capsys.readouterr().out
    assert "Unknown option" in out
    assert "usage: spc submit" in out


def test_submit_missing_app(app, monkeypatch, tmp_path, capsys):
    _set_user_data_root(monkeypatch, tmp_path)

    _run_cli_expect_exit(monkeypatch, ["spc", "submit", "not_an_app"])
    out = capsys.readouterr().out
    assert "app 'not_an_app' not found" in out


def test_status_missing_case_id(app, monkeypatch, tmp_path, capsys):
    _set_user_data_root(monkeypatch, tmp_path)

    _run_cli_expect_exit(monkeypatch, ["spc", "status"])
    out = capsys.readouterr().out
    assert "usage: spc status <case_id>" in out


def test_cases_listing(app, monkeypatch, tmp_path, capsys):
    _set_user_data_root(monkeypatch, tmp_path)

    _run_cli(monkeypatch, ["spc", "submit", "dna", "--params", "dna=ATCG"])
    capsys.readouterr()

    _run_cli(monkeypatch, ["spc", "cases"])
    out = capsys.readouterr().out
    assert "CID" in out
    assert "APP" in out
    assert "STATUS" in out
    assert "dna" in out


def test_status_unknown_case(app, monkeypatch, tmp_path, capsys):
    _set_user_data_root(monkeypatch, tmp_path)

    _run_cli_expect_exit(monkeypatch, ["spc", "status", "nope"])
    out = capsys.readouterr().out
    assert "ERROR: case 'nope' not found" in out


def test_cases_help_and_filters(app, monkeypatch, tmp_path, capsys):
    _set_user_data_root(monkeypatch, tmp_path)

    _run_cli_expect_exit(monkeypatch, ["spc", "cases", "--help"])
    out = capsys.readouterr().out
    assert "usage: spc cases" in out

    _run_cli_expect_exit(monkeypatch, ["spc", "cases", "--user", "missing_user"])
    out = capsys.readouterr().out
    assert "No cases found for user 'missing_user'" in out

    _run_cli_expect_exit(monkeypatch, ["spc", "cases", "--state", "R"])
    out = capsys.readouterr().out
    assert "No cases found" in out


def test_scheduler_command(app, monkeypatch, tmp_path, capsys):
    _set_user_data_root(monkeypatch, tmp_path)
    calls = {}

    class DummyScheduler:
        def __init__(self):
            calls["init"] = True

        def poll(self):
            calls["poll"] = True

    import spc.scheduler as scheduler
    monkeypatch.setattr(scheduler, "Scheduler", DummyScheduler)

    def pre_main(cli):
        def fake_sleep(_):
            raise KeyboardInterrupt()
        cli.time.sleep = fake_sleep

    _run_cli(monkeypatch, ["spc", "scheduler"], pre_main=pre_main)
    out = capsys.readouterr().out
    assert "Starting SPC scheduler" in out
    assert "Scheduler stopped." in out
    assert calls.get("poll") is True


def test_shell_scheduler_and_tail(app, monkeypatch, tmp_path, capsys):
    _set_user_data_root(monkeypatch, tmp_path)

    class DummyScheduler:
        def poll(self):
            return None

    import spc.scheduler as scheduler
    monkeypatch.setattr(scheduler, "Scheduler", DummyScheduler)

    commands = iter([
        "start",
        "tail missing",
        "stop",
        "quit",
    ])

    def fake_input(_prompt=""):
        return next(commands)

    monkeypatch.setattr(builtins, "input", fake_input)

    _run_cli(monkeypatch, ["spc", "shell"])
    out = capsys.readouterr().out
    assert "Scheduler started" in out
    assert "Case 'missing' not found" in out
    assert "Scheduler stopped" in out
