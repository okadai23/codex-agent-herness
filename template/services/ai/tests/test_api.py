from pathlib import Path


def test_health_endpoint_defined() -> None:
    source = (Path(__file__).resolve().parents[1] / "src" / "api" / "main.py").read_text(encoding="utf-8")
    assert '@app.get("/health")' in source
