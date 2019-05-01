#!/usr/bin/env python3
import pkgutil
from typing import Iterable

__path__: Iterable[str] = pkgutil.extend_path(__path__, __name__)

from qcc.qcc import init, compile, get_profiles
