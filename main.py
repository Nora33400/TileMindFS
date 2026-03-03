import argparse
import logging

from engine import TileStore
from optimizer import Optimizer
from tilemindfs.config import load_config
from tilemindfs.dispatcher import Dispatcher
from tilemindfs.logging_utils import configure_logging
from tilemindfs.models import BudgetModel, CoherenceModel, ScoreEngine
from tilemindfs.planner import Planner, load_jobs, plan_to_json, plan_to_text


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="tilemindfs",
        description="Tile-based dedup + resource-aware dry-run planner.",
    )
    parser.add_argument("--config", default="config.yaml", help="Path to YAML configuration")

    sub = parser.add_subparsers(dest="command")

    store_p = sub.add_parser("store", help="Store a file into tiles")
    store_p.add_argument("file")

    rec_p = sub.add_parser("reconstruct", help="Reconstruct a stored file")
    rec_p.add_argument("original")
    rec_p.add_argument("output")

    sub.add_parser("report", help="Print storage report")

    opt_p = sub.add_parser("optimize", help="Run optimizer loop")
    opt_p.add_argument("--interval", type=int, default=5)

    plan_p = sub.add_parser("plan", help="Create manual-guided dry-run plan")
    plan_p.add_argument("--jobs", required=True, help="JSON file containing candidate jobs")
    plan_p.add_argument("--dry-run", action="store_true", help="Required safety switch; planner never executes")
    plan_p.add_argument("--resource-limit", type=float, default=None, help="Override budget limit from config")
    plan_p.add_argument("--top-k", type=int, default=None, help="Override top-k from config")
    plan_p.add_argument("--output", choices=["text", "json"], default="text")

    args = parser.parse_args()

    if args.command in {"plan", "optimize"}:
        cfg = load_config(args.config)
        configure_logging(cfg.logging.level)
        logger = logging.getLogger("tilemindfs.cli")
    else:
        cfg = None
        logger = None

    if args.command == "store":
        print(TileStore().store_file(args.file))
    elif args.command == "reconstruct":
        print(TileStore().reconstruct_file(args.original, args.output))
    elif args.command == "report":
        print(TileStore().report())
    elif args.command == "optimize":
        Optimizer().run_loop(args.interval)
    elif args.command == "plan":
        if not args.dry_run:
            parser.error("Manual-guided mode only: pass --dry-run")

        jobs = load_jobs(args.jobs)
        score_engine = ScoreEngine(cfg.weights, CoherenceModel())
        planner = Planner(score_engine, Dispatcher(BudgetModel()))

        limit = args.resource_limit if args.resource_limit is not None else cfg.budget.default_resource_limit
        top_k = args.top_k if args.top_k is not None else cfg.planner.default_top_k

        result = planner.plan(jobs=jobs, resource_limit=limit, top_k=top_k)
        logger.info(
            "dry-run plan generated count_selected=%s total_resource=%s",
            len(result.selected),
            result.total_resource,
        )
        print(plan_to_json(result) if args.output == "json" else plan_to_text(result))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
