# python-boundary-rules

- domain/application に FastAPI, provider SDK, DB client を直接入れない。
- infrastructure/adapters で I/O 実装し、port/interface 経由で接続する。
- verify: `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`。
