#!/usr/bin/env python3
"""
KAREN11 Runtime Harness V1
System: JOY / AL
Author: Jay Wisdom
Authority: false

Purpose:
Evaluate a claim against the Minnesota Math ladder without allowing
unsupported promotion, narrative drift, or authority inflation.

Ladder:
UNKNOWN -> OBSERVED -> FETCHED -> PRESERVED -> VERIFIED -> REPLAYABLE
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
import json
import re
from typing import List, Optional, Dict, Any


SHA256_RE = re.compile(r"^[a-f0-9]{64}$")


class State(str, Enum):
    UNKNOWN = "UNKNOWN"
    OBSERVED = "OBSERVED"
    FETCHED = "FETCHED"
    PRESERVED = "PRESERVED"
    VERIFIED = "VERIFIED"
    REPLAYABLE = "REPLAYABLE"


@dataclass