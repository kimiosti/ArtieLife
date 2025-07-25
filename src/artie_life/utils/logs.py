"""Module containing utilities for logging."""
from typing import TYPE_CHECKING
from os.path import join as join_path

if TYPE_CHECKING:
    from typing import Callable

LOGS_FOLDER: "str" = "logs"
WORLD_LOG: "str" = join_path(LOGS_FOLDER, "world", "log")
ATTENTION_LOG: "Callable[[int], str]" = \
        lambda living_id: join_path(LOGS_FOLDER, str(living_id), "attention")
REASON_LOG: "Callable[[int], str]" = \
        lambda living_id: join_path(LOGS_FOLDER, str(living_id), "reason")
GENOME_LOG: "Callable[[int], str]" = \
        lambda living_id: join_path(LOGS_FOLDER, str(living_id), "genome")
