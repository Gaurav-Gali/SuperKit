"""
SuperKit
--------

A batteries-included, opinionated framework built on FastAPI
that provides structure, conventions, and tooling without hiding
how things work.
"""

# Application factory
from superkit.api.app_factory import create_app

# Public contracts
from superkit.apps.config import AppConfig
from superkit.routing.router import Router

__all__ = [
    "create_app",
    "AppConfig",
    "Router",
]
