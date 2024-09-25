"""Access to configuration data"""
import os
from functools import lru_cache
from typing import Optional

import yaml

import conf.default as default
import conf.settings as settings


def get_feature_flag(name: str, module=None, fallback_module=None):
    return module.__dict__.get(name, fallback_module.__dict__.get(name))


def get_ff(name: str) -> Optional[str]:
    value = os.environ.get(name)
    return (
        value
        if value
        else get_feature_flag(name=name, module=settings, fallback_module=default)
    )


@lru_cache
def load_yaml(name: str, folder: str = "conf") -> dict:
    path = os.path.join(folder, name)
    with open(path, "r") as fp:
        return yaml.safe_load(stream=fp)
