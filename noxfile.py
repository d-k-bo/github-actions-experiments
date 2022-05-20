import nox

nox.options.sessions = ["format", "lint", "mypy", "test"]


@nox.session
def format(session: nox.Session):
    session.install("black", "isort")
    session.run("isort", ".")
    session.run("black", ".")


@nox.session
def check_format(session: nox.Session):
    session.install("black", "isort")
    session.run("isort", ".", "--check")
    session.run("black", ".", "--check")


@nox.session
def lint(session: nox.Session):
    session.install(
        "pyproject-flake8",
        "flake8-annotations",
        "flake8-bugbear",
        "flake8-docstrings",
    )
    session.run("pflake8")


@nox.session
def mypy(session: nox.Session) -> None:
    session.install(".[test]", "mypy")
    session.run("mypy")


@nox.session(python=["3.8", "3.9", "3.10", "3.11", "pypy3"])
def test(session: nox.Session):
    session.install(".[test]", "coverage")
    try:
        session.run("coverage", "run", "-m", "pytest")
    finally:
        session.run("coverage", "report")


@nox.session(python=False)
def venv(session: nox.Session):
    import pathlib

    venv_path = pathlib.Path("venv").absolute()

    session.run("python", "-m", "venv", "venv")
    session.run(
        str(venv_path / "bin/python"), "-m", "pip", "install", "-U", "pip", "wheel"
    )
    session.run(str(venv_path / "bin/pip"), "install", ".[test]")
