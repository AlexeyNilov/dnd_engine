"""Access to configuration data"""
import os
from typing import Optional

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
