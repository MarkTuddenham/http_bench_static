from typing import List

from dataclasses import dataclass

@dataclass
class APIArgs:
    """The parameters given in a request to the API."""

    text: str
    count: int


@dataclass
class APIResponse:
    """The parameters returned from the request."""

    texts: List[str]

