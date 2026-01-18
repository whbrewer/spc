#!/usr/bin/env python3
"""SPC MCP server exposing apps as MCP tools over HTTP."""

from __future__ import annotations

import argparse
import os
import time
from typing import Any, Dict, Optional

import anyio
from mcp.server.fastmcp import FastMCP
from . import config, migrate
from .common import rand_cid, replace_tags


def _get_app_instance(app_name: str, input_format: str):
    from . import app_reader_writer as apprw

    if input_format == "namelist":
        return apprw.Namelist(app_name)
    if input_format == "ini":
        return apprw.INI(app_name)
    if input_format == "json":
        return apprw.JSON(app_name)
    if input_format == "yaml":
        return apprw.YAML(app_name)
    if input_format == "toml":
        return apprw.TOML(app_name)
    if input_format == "xml":
        return apprw.XML(app_name)
    return apprw.INI(app_name)


def _submit_job(
    app_name: str,
    params: Optional[Dict[str, Any]] = None,
    desc: str = "",
    np: int = 1,
    user: str = "mcp",
) -> Dict[str, Any]:
    from . import app_reader_writer as apprw

    dal = migrate.dal(uri=config.uri)
    db = dal.db

    app_row = db(db.apps.name == app_name).select().first()
    if not app_row:
        return {"error": f"app '{app_name}' not found"}

    user_row = db(db.users.user == user).select().first()
    if not user_row:
        uid = db.users.insert(user=user, passwd="", priority=3)
        db.commit()
        user_row = db(db.users.id == uid).select().first()
    uid = user_row.id

    cid = rand_cid()
    input_format = app_row.input_format or "ini"
    myapp = _get_app_instance(app_name, input_format)

    run_params: Dict[str, Any] = dict(myapp.params) if getattr(myapp, "params", None) else {}
    run_params.update({"case_id": cid, "cid": cid, "user": user})
    if params:
        for key, val in params.items():
            run_params[str(key)] = str(val)

    myapp.write_params(run_params, user)

    cmd = app_row.command or f"./{app_name}"
    run_params["rel_apps_path"] = (os.pardir + os.sep) * 4 + apprw.apps_dir
    cmd = replace_tags(cmd, run_params)

    jid = db.jobs.insert(
        uid=uid,
        app=app_name,
        cid=cid,
        command=cmd,
        state="Q",
        description=desc or "",
        time_submit=time.strftime("%a %b %d %H:%M:%S %Y"),
        walltime=3600,
        np=np,
        priority=user_row.priority or 3,
    )
    db.commit()

    return {
        "app": app_name,
        "cid": cid,
        "jid": str(jid),
        "state": "Q",
    }


def _get_status(cid: str) -> Dict[str, Any]:
    dal = migrate.dal(uri=config.uri)
    db = dal.db
    job = db(db.jobs.cid == cid).select().first()
    if not job:
        return {"error": f"case '{cid}' not found"}

    user_row = db(db.users.id == job.uid).select().first()
    username = user_row.user if user_row else "unknown"
    return {
        "cid": cid,
        "jid": str(job.id),
        "app": job.app,
        "user": username,
        "state": job.state,
        "description": job.description or "",
        "time_submit": job.time_submit,
        "np": job.np,
    }


def _list_cases(
    app: Optional[str] = None,
    user: Optional[str] = None,
    state: Optional[str] = None,
    limit: int = 20,
) -> Dict[str, Any]:
    dal = migrate.dal(uri=config.uri)
    db = dal.db

    query = db.jobs.id > 0
    if app:
        query &= db.jobs.app == app
    if state:
        query &= db.jobs.state == state
    if user:
        user_row = db(db.users.user == user).select().first()
        if not user_row:
            return {"count": 0, "cases": []}
        query &= db.jobs.uid == user_row.id

    jobs = db(query).select(orderby=~db.jobs.id, limitby=(0, limit))
    cases = []
    for job in jobs:
        user_row = db(db.users.id == job.uid).select().first()
        cases.append(
            {
                "cid": job.cid,
                "jid": str(job.id),
                "app": job.app,
                "user": user_row.user if user_row else "unknown",
                "state": job.state,
                "description": job.description or "",
                "time_submit": job.time_submit,
            }
        )
    return {"count": len(cases), "cases": cases}


def _list_apps() -> Dict[str, Any]:
    dal = migrate.dal(uri=config.uri)
    db = dal.db
    apps = []
    for row in db(db.apps.id > 0).select(orderby=db.apps.name):
        apps.append(
            {
                "name": row.name,
                "description": row.description or "",
                "input_format": row.input_format or "ini",
                "command": row.command or "",
            }
        )
    return {"count": len(apps), "apps": apps}


def create_mcp_server() -> FastMCP:
    mcp = FastMCP(
        "spc-mcp",
        instructions="Run SPC apps and query runs via MCP over HTTP.",
    )

    @mcp.tool(name="list_apps")
    async def list_apps_tool() -> Dict[str, Any]:
        return _list_apps()

    @mcp.tool(name="list_cases")
    async def list_cases_tool(
        app: Optional[str] = None,
        user: Optional[str] = None,
        state: Optional[str] = None,
        limit: int = 20,
    ) -> Dict[str, Any]:
        return _list_cases(app=app, user=user, state=state, limit=limit)

    @mcp.tool(name="get_status")
    async def get_status_tool(cid: str) -> Dict[str, Any]:
        return _get_status(cid)

    # Register one tool per app
    apps = _list_apps().get("apps", [])

    for app in apps:
        app_name = app["name"]
        app_desc = app.get("description") or f"Run the {app_name} app"

        def _make_run_tool(app_name: str, description: str):
            @mcp.tool(name=f"run_{app_name}", description=description)
            async def run_app_tool(
                params: Optional[Dict[str, Any]] = None,
                desc: str = "",
                np: int = 1,
                user: str = "mcp",
            ) -> Dict[str, Any]:
                return _submit_job(app_name, params=params, desc=desc, np=np, user=user)

            return run_app_tool

        _make_run_tool(app_name, app_desc)

    return mcp


def main() -> None:
    parser = argparse.ArgumentParser(description="SPC MCP server (HTTP)")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7333)
    parser.add_argument("--path", default="/mcp")
    args = parser.parse_args()

    mcp = create_mcp_server()
    anyio.run(
        lambda: mcp.run_streamable_http_async(
            host=args.host,
            port=args.port,
            streamable_http_path=args.path,
        )
    )


if __name__ == "__main__":
    main()
