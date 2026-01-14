# SPC — Scientific Platform for the Cloud

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Docs](https://img.shields.io/badge/docs-Read%20the%20Docs-blue.svg)](http://spc.readthedocs.io)

> Note: See `NOTES.md` for important release notes.

Full documentation is available online at: http://spc.readthedocs.io  
Minimum Python requirement: **3.8** (tested on **3.12**).

---

## Overview

The **Scientific Platform for the Cloud (SPC)** is a Python-based platform/framework for rapidly migrating and running **scientific applications** in the cloud. SPC provides a web UI and workflow scaffolding for running parameterized simulations, tracking cases, managing files, executing jobs through a scheduler, and visualizing results (including plotting) in a standardized and repeatable way.

This repository contains the **Python 3 modernization** of SPC, built with:
- **Flask + Jinja2** (web UI stack)
- **pydal** (data layer)
- **boto3** (AWS integration)

The original Python 2 / Bottle implementation is archived in the `legacy` branch:
https://github.com/whbrewer/spc/tree/legacy

---

## Features (High-level)

- Web-based UI for launching and monitoring scientific workflows
- Standardized parameter entry and input deck generation
- Case management and file management per run
- Job submission and output redirection
- Plot definitions and result visualization
- Packaged “apps” that can be installed into SPC

---

## Best fit / Intended use

SPC is ideally suited for scientific applications that:

1. Use an **input deck** of common parameter types (ints, floats, strings, booleans) stored in standardized formats such as:
   - INI, XML, JSON, YAML, TOML, or `Namelist.input`
2. Require **non-trivial runtime** (though instantaneous jobs are supported)
3. Produce **plots** and/or structured results
4. Use **MPI** or MapReduce for parallelization (serial workflows are also supported)

Other applications may be supported with additional pre-/post-processing.

---

## Screenshots

![SPC UI](docs/_static/spc0.png)
![SPC UI](docs/_static/spc1.png)
![SPC UI](docs/_static/spc2.png)

---

## Requirements

SPC assumes the following are available on your system:

### System prerequisites
- Python **3.8+**
- `virtualenv` (or equivalent environment tooling)
- A compiler toolchain (`gcc` / `clang`)
- Python development headers (required to build packages such as `psutil`)
  - Debian/Ubuntu: `python3-dev`
  - RHEL/CentOS: `python3-devel`

### Browser support
SPC has been tested primarily with **Google Chrome** on Linux and macOS. Other environments may work but are not guaranteed.

---

## Quickstart

Initialize SPC (installs dependencies and initializes the SPC database):

```bash
./spc init
```

Start the web server:

```bash
./spc run
```

Open your browser at:

- http://localhost:8580/

> Note: Port can be overridden in `config.py`.

---

## Run the pre-installed example: DNA Analyzer

1. **Activate App**  
   Navigate to `Apps` → `Installed`.  
   Click **Activate** for the DNA app, then return to `Activated`.

2. **Enter Parameters**  
   Open the `dna` app and enter a DNA string (or use the default).  
   Click `confirm` to write the datafile to disk.

3. **Start Job**  
   Click `execute` to run the DNA analysis.  
   SPC will submit the job to the scheduler and redirect to the output view.

4. **Inspect Outputs**  
   Use `files` to open the file manager.  
   Use `output` to view redirected executable output.  
   Use `download` to zip and download all case files.

5. **View Plots**  
   Click `plot` to define/view plots.  
   Use `data` to view the plotted data files (also visible via `files`).

---

## Install packaged apps

To install an SPC packaged app (example: Mendel’s Accountant), run one of:

### macOS (Apple Silicon)
```bash
./spc install https://github.com/whbrewer/spc-fmendel-plugin/releases/download/v2.0.1/fmendel-spc-darwin-arm64.zip
```

### Linux (x86_64)
```bash
./spc install https://github.com/whbrewer/spc-fmendel-plugin/releases/download/v2.0.1/fmendel-spc-linux-x86_64.zip
```

---

## Documentation

- Online documentation: http://spc.readthedocs.io
- Local docs: see the `docs/` directory

---

## Developer setup (minimal)

A lightweight development workflow:

1. Clone the repo and enter it:
```bash
git clone https://github.com/whbrewer/spc.git
cd spc
```

2. Initialize SPC:
```bash
./spc init
```

3. Run the server:
```bash
./spc run
```

4. Open:
- http://localhost:8580/

### Suggested additions (optional, if/when present)
If you add these, document them here:
- Unit tests: `pytest`
- Linting: `ruff`
- Formatting: `black`
- Type checking: `mypy`

---

## Contributing

Contributions are welcome.

Suggested workflow:
1. Fork the repo
2. Create a feature branch
3. Make changes with clear commit messages
4. Add/update documentation where needed
5. Open a Pull Request

If you plan to contribute a new packaged app/plugin, please include:
- A small example input deck
- A minimal runnable executable or script stub
- One representative plot/output artifact

---

## Citation

If you use SPC in academic work, please cite:

> W. Brewer, W. Scott, and J. Sanford, “An Integrated Cloud Platform for Rapid Interface Generation, Job Scheduling, Monitoring, Plotting, and Case Management of Scientific Applications”, Proc. of the International Conference on Cloud Computing Research and Innovation, Singapore, IEEE Press, October 2015, pp. 156–165. DOI: 10.1109/ICCCRI.2015.24

---

## Support / Questions

For questions, contact [Wes Brewer](https://www.ornl.gov/staff-profile/wes-h-brewer).
