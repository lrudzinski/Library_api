import os

import nox

nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = ["check_isort", "check_flake", "check_black", "check_pylint", "check_tests"]

FLAKE_DJANGO_VERSION = "flake8-django==1.4"
FLAKE_VERSION = "flake8==6.1.0"
PYLINT_DJANGO_VERSION = "pylint-django==2.5.5"
PYLINT_VERSION = "pylint==3.2.7"
AUTOFLAKE_VERSION = "autoflake==2.3.1"
BLACK_VERSION = "black==24.8.0"
ISORT_VERSION = "isort==5.13.2"
PYTEST_VERSION = "pytest==8.3.3"
PYTEST_DJANGO_VERSION = "pytest-django==4.9.0"
PYTEST_COV_VERSION = "pytest-cov==5.0.0"
CONFIG_PATH = "configuration/pyproject.toml"
ENVS = {
    "POSTGRES_HOST": os.getenv("POSTGRES_HOST"),
    "POSTGRES_DB": os.getenv("POSTGRES_DB"),
    "POSTGRES_USER": os.getenv("POSTGRES_USER"),
    "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD"),
    "DJANGO_SETTINGS_MODULE": "library_api.settings",
}


@nox.session()
def check_tests(session):
    """Run the test suite."""
    session.install("-r", "requirements.txt")
    session.install(PYTEST_VERSION, PYTEST_DJANGO_VERSION)
    session.run("pytest", *session.posargs, env=ENVS)


@nox.session()
def check_black(session):
    """Check code compatibility with black"""
    session.install(BLACK_VERSION)
    session.run(
        "black",
        "--config",
        CONFIG_PATH,
        "--check",
        "--diff",
        "--color",
        ".",
    )


@nox.session()
def check_flake(session):
    """Check code compatibility with flake8"""
    session.install(FLAKE_VERSION, FLAKE_DJANGO_VERSION)
    session.run("flake8", "--config", "configuration/.flake8", ".")


@nox.session()
def check_isort(session):
    """Check if imports are sorted correctly"""
    session.install(ISORT_VERSION)
    session.run("isort", "--sp", CONFIG_PATH, "--check-only", "--diff", ".")


@nox.session()
def check_pylint(session):
    """Check code compatibility with check pylint with django_lint"""
    session.install("-r", "requirements.txt")
    session.install(PYLINT_VERSION, PYLINT_DJANGO_VERSION)
    session.run(
        "pylint",
        "--load-plugins=pylint_django",
        "--recursive=true",
        f"--rcfile={CONFIG_PATH}",
        ".",
        env=ENVS,
    )


@nox.session()
def format_code(session):
    """Format code according to rules used in project"""
    session.install(BLACK_VERSION, ISORT_VERSION, AUTOFLAKE_VERSION)
    session.run("isort", "--sp", CONFIG_PATH, ".")
    session.run(
        "autoflake",
        "--remove-unused-variables",
        "--remove-all-unused-imports",
        "--in-place",
        "--recursive",
        "--exclude=migrations",
        ".",
    )
    session.run("black", "--config", CONFIG_PATH, ".")
