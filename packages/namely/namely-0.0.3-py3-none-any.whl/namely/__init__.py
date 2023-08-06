"""Namely Python Client"""
__title__ = "namely"
__version__ = "0.0.3"
__license__ = "MIT"
__copyright__ = "Copyright 2021 Vadym Khodak"

from .client import Client  # noqa


def get_version() -> str:
    return __version__
