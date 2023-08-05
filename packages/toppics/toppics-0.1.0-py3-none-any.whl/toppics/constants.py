import re
from typing import Dict, List, Pattern

# Topic lists
PYTHON_CLI_TOPICS: List[str] = ["python", "cli"]

TOPICS: Dict[str, List[str]] = {"Python CLI": PYTHON_CLI_TOPICS}

# GitHub
# More info:
# - https://github.com/FriendCode/giturlparse.py
# - https://github.com/nephila/giturlparse
WEB_URL_PATTERN: Pattern[str] = re.compile(
    r"https://github.com/(?P<owner>.+)/(?P<repo>.+)"
)

DEFAULT_ENV_VARIABLE: str = "GITHUB_TOKEN"

# CLI
TOKEN_HELP: str = "The GitHub personal access token."
URL_ERROR_MSG: str = "it must be an HTTPS/web URL for a GitHub repo."
