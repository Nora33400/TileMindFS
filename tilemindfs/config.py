from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class Weights:
    lambda_: float
    mu: float
    rho: float
    eta: float


@dataclass(frozen=True)
class BudgetConfig:
    default_resource_limit: float


@dataclass(frozen=True)
class PlannerConfig:
    default_top_k: int


@dataclass(frozen=True)
class LoggingConfig:
    level: str


@dataclass(frozen=True)
class AppConfig:
    seed: int
    weights: Weights
    budget: BudgetConfig
    planner: PlannerConfig
    logging: LoggingConfig


def load_config(path: str | Path = "config.yaml") -> AppConfig:
    with Path(path).open("r", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)

    weights = Weights(
        lambda_=float(raw["weights"]["lambda"]),
        mu=float(raw["weights"]["mu"]),
        rho=float(raw["weights"]["rho"]),
        eta=float(raw["weights"]["eta"]),
    )
    budget = BudgetConfig(default_resource_limit=float(raw["budget"]["default_resource_limit"]))
    planner = PlannerConfig(default_top_k=int(raw["planner"]["default_top_k"]))

    if budget.default_resource_limit <= 0:
        raise ValueError("budget.default_resource_limit must be > 0")
    if planner.default_top_k <= 0:
        raise ValueError("planner.default_top_k must be > 0")

    return AppConfig(
        seed=int(raw["seed"]),
        weights=weights,
        budget=budget,
        planner=planner,
        logging=LoggingConfig(level=str(raw["logging"]["level"])),
    )
