from pathlib import Path


WORKSPACE_DIRS = [
    "workspace/cache",
    "workspace/findings",
    "workspace/findings/raw",
    "workspace/memory",
    "workspace/reports",
    "workspace/scratch",
    "workspace/topics",
]


def ensure_workspace():
    for directory in WORKSPACE_DIRS:
        Path(directory).mkdir(
            parents=True,
            exist_ok=True,
        )