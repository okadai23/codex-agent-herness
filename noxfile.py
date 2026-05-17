import nox

nox.options.sessions = ["ruff", "pytest", "pyright"]


@nox.session(python=False)
def ruff(session: nox.Session) -> None:
    session.run("uv", "run", "ruff", "check", "scripts", "tests")


@nox.session(python=False)
def pytest(session: nox.Session) -> None:
    session.run("uv", "run", "pytest")


@nox.session(python=False)
def pyright(session: nox.Session) -> None:
    session.run("uv", "run", "pyright")
