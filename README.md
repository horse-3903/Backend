<div align="center">

# Backend

Flask REST API backend for the Hwa Chong Discord Bot

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/github/license/horse-3903/Backend?style=flat-square)](LICENSE)

> **Note:** This is a fork of the original Hwa Chong Discord Bot backend.

</div>

---

## Overview

A lightweight Flask REST API that serves layout data and manages a SQLite database for the [Hwa Chong Discord Bot](https://github.com/horse-3903/Discord-Bot). Exposes API routes consumed by the bot's frontend commands.

## Tech Stack

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)

## Getting Started

### Prerequisites

- Python 3.8+
- Flask

```bash
pip install flask
```

### Running Locally

```bash
python src/main.py
```

You can inspect the SQLite database using [DB Browser for SQLite](https://sqlitebrowser.org).

## API Reference

| Method | Route | Description |
|--------|-------|-------------|
| `GET` | `/api/v1/layout` | Returns the full layout configuration |

All available routes are also defined in [`src/layout.json`](src/layout.json).

## Project Structure

```
Backend/
├── src/
│   ├── main.py              # Flask app entry point
│   ├── database_columns.py  # Database schema definitions
│   ├── sql_funcs.py         # SQLite helper functions
│   ├── extern_funcs.py      # External utility functions
│   ├── layout.json          # API route definitions
│   └── database.db          # SQLite database
└── README.md
```

## License

MIT License — see [LICENSE](LICENSE) for details.
