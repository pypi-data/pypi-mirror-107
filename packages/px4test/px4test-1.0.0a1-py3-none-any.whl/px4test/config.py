from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

from pydantic import BaseModel


class Px4TestConfig(BaseModel):
    log_dest: Optional[Path] = None
    mission_dest: Optional[Path] = None
