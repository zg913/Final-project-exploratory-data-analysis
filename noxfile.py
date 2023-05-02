from nox import Session
import nox

# default session

nox.options.sessions = ["flake8", "black", "test"]


# flakes style check pep8
@nox.session(name="flake8")
def flake8(session: Session) -> None:
    session.install("flake8")
    session.run("flake8", "final.py", "noxfile.py", "tests")


# black style check
@nox.session(name="black")
def black(session: Session) -> None:
    session.install("black")
    session.run("black", "final.py", "noxfile.py", "tests")


# test
@nox.session(name="test")
def run_test(session: Session) -> None:
    session.install("pytest")
    session.run("pip", "install", "-r", "requirements.txt")
    session.install(".")
    session.run("pytest", "-v", "tests")
