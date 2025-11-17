# AI Tools Demo

This repository hosts a lightweight GUI showcasing how various AI tools can bootstrap a small user-database viewer. Every component—from the Qt interface to the tests—was assembled collaboratively by different AI assistants to demonstrate their utility in day-to-day software engineering tasks.

## Features
- Login screen with email/password validation helpers.
- Welcome screen that greets the authenticated user.
- Database tab displaying mocked user records from `data/mock_users.json`.
- Dashboard tab summarising usage metrics (active users, login counts, role distribution).
- Pytest + qtbot suite that exercises key UI flows.

## Installation
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install --upgrade pip
pip install .              # add [test] to pull pytest dependencies
```

The project is packaged with `pyproject.toml` (Hatchling backend) so it can be installed via `pip install .` or `pip install -e .` for editable development.

## Running the App
```bash
python ui.py
```

Use the credentials `admin@example.com` / `Admin123!` to experience the post-login workspace. The mock DB lives in `data/mock_users.json`; updating that file will automatically refresh the table and dashboard the next time the app loads data.

## Running Tests
```bash
pip install .[test]
pytest
```

The test suite uses `pytest-qt` with an off-screen Qt platform so it runs headlessly in CI environments.

## Repository Structure
```
ai_tools_demo/
├── data/mock_users.json   # mock database
├── ui.py                  # Qt UI components (login + workspace)
├── utils.py               # validation helpers and data access
├── tests/test_ui.py       # pytest/qtbot coverage
└── pyproject.toml         # packaging metadata
```

## Credits
This entire project was produced by a collection of AI coding assistants to illustrate what modern AI tools can deliver with minimal human intervention. Feel free to reuse it as a starting point or as a teaching aid when discussing AI-driven development.
