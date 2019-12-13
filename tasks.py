from pathlib import Path

from invoke import task
from nox.virtualenv import VirtualEnv

# Configuration values.
VENV = "venv"

@task
def build(c):
    """Build the documentatrion site."""
    mkdocs = mkdocs_bin()
    c.run(f'{mkdocs} build -v -s')

@task
def publish(c):
    """Publish the site to github pages."""
    mkdocs = mkdocs_bin()
    c.run(f'{mkdocs} gh-deploy -v --clean')


@task()
def serve(c):
    """Serve the documentation using the development server."""
    mkdocs = mkdocs_bin()
    c.run(f'{mkdocs} serve')

@task(default=True)
def setup(c):
    """Setup the student environment."""
    c.run("python3 -m venv venv")
    _, venv_bin, _ = get_venv(VENV)
    pip = venv_bin / "pip"
    c.run(f"{pip.resolve()} install -U pip setuptools")
    c.run(f"{pip.resolve()} install -r requirements.txt -r requirements-dev.txt")


@task
def resize_images(c):
    """Resize images for the BNA document."""
    with c.cd("images-orig"):
        c.run("mogrify -resize 180x -path ../docs/images *.png")


def get_venv(venv):
    """
    Return `Path` objects from the venv.
    :param str venv: venv name
    :return: the venv `Path`, the `bin` folder `Path` within the venv, and if specified, the `Path` object of the
        activate script within the venv.
    :rtype: a tuple of 3 `Path` objects.
    """
    location = Path(venv)
    venv = VirtualEnv(location.resolve())
    venv_bin = Path(venv.bin)
    activate = venv_bin / "activate"
    return venv, venv_bin, activate

def mkdocs_bin():
    _,venv_bin,_ = get_venv(VENV)
    return venv_bin / "mkdocs"
