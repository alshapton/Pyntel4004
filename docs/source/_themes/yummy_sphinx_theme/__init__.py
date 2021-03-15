"""
Yummy Sphinx Theme, created to mirror Yummy-Jekyll for sphinx
"""
from os import path

__version__ = '0.1.1'


def get_path():
    """Return list of HTML theme paths."""
    return path.abspath(path.dirname(path.dirname(__file__)))


def setup(app):
    app.add_html_theme('yummy_sphinx_theme', path.abspath(path.dirname(__file__)))
    return {'version': __version__}
