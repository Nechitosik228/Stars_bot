from enum import Enum


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return self.value


from . git import GitHubCommands
from . venv import VenvCommands