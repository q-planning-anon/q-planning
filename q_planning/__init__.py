"""Q-Planning: value-guided action selection and self-improvement for frozen policies.

Importing this package prepares the process environment (see :mod:`q_planning._env_setup`)
**before** anything can pull in LeRobot, which is what stops the pinned fork's built-in
cluster path for the Wan2.2 weights from taking effect. Everything else is imported lazily,
so ``import q_planning`` stays cheap and never drags in torch.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from q_planning._env_setup import (
    EnvironmentAlreadyImported,
    add_robotwin_to_path,
    describe_environment,
    prepare_environment,
)

# Apply whatever the user already exported. A config-driven call in q_planning.cli refines
# this once a run config has been resolved; because prepare_environment() never overwrites
# an existing variable, the two calls compose rather than fight.
prepare_environment(strict=False)

__version__ = "1.0.0"

# The pinned commit of https://github.com/q-planning-anon/lerobot this package builds on.
# Kept here so `q-planning doctor` can report drift between the installed fork and this pin.
LEROBOT_PIN = "q-planning-release-v1"

if TYPE_CHECKING:  # pragma: no cover - import-time cost is the whole point of deferring
    from q_planning.planner import NoPlanner, QWeightedPlanner
    from q_planning.policies.base import BCBundle, BCChunkSampler
    from q_planning.policy import QPlanningPolicy

_LAZY: dict[str, str] = {
    "QWeightedPlanner": "q_planning.planner",
    "NoPlanner": "q_planning.planner",
    "QPlanningPolicy": "q_planning.policy",
    "BCChunkSampler": "q_planning.policies.base",
    "BCBundle": "q_planning.policies.base",
}


def __getattr__(name: str) -> Any:
    """Resolve the heavy public symbols on first use (PEP 562)."""
    module = _LAZY.get(name)
    if module is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    import importlib

    return getattr(importlib.import_module(module), name)


def __dir__() -> list[str]:
    return sorted([*globals(), *_LAZY])


__all__ = [
    "LEROBOT_PIN",
    "BCBundle",
    "BCChunkSampler",
    "EnvironmentAlreadyImported",
    "NoPlanner",
    "QPlanningPolicy",
    "QWeightedPlanner",
    "__version__",
    "add_robotwin_to_path",
    "describe_environment",
    "prepare_environment",
]
