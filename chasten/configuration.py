"""Configuration for Chasten."""

from pathlib import Path
from typing import List

from pydantic import BaseModel


class ChastenConfiguration(BaseModel):
    """Configuration of Chasten."""

    directory: List[Path]
