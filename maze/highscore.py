import re
from typing import Any, Dict, List


MAX_ENTRIES = 10
MAX_NAME_LENGTH = 10
DEFAULT_NAME = "PLAYER"

_VALID_NAME_CHARS = re.compile(r"[^A-Za-z0-9 ]")

EMPTY_HIGHSCORES: List[Dict[str, Any]] = []
