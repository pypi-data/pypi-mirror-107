from hashlib import md5
from json import dump as json_dump
from typing import List, TypedDict, Sequence

from click import command, argument
from pydantic.errors import MissingError
from staliro import staliro
from staliro.results import Iteration
from staliro.specification import Specification

from .blackbox import px4_blackbox_factory
from .module import load_module


class IterationDict(TypedDict, total=False):
    sample: List[float]
    robustness: float
    sample_hash: str


class RunDict(TypedDict):
    num: int
    iterations: List[IterationDict]


def _iter_dict(iteration: Iteration, with_hash: bool = False) -> IterationDict:
    if not with_hash:
        return IterationDict(
            sample=list(iteration.sample),
            robustness=iteration.robustness,
        )

    return IterationDict(
        sample=list(iteration.sample),
        robustness=iteration.robustness,
        sample_hash=md5(iteration.sample.tobytes()).hexdigest(),
    )


def _run_dict(num: int, history: Sequence[Iteration], with_hash: bool = False) -> RunDict:
    return RunDict(num=num, iterations=[_iter_dict(iteration, with_hash) for iteration in history])


@command()
@argument("module_name")
def px4test(module_name: str) -> None:
    module = load_module(module_name)
    blackbox = px4_blackbox_factory(module.config, module.stack_config, module.mission_factory)
    specification = Specification(module.phi, module.predicates)

    log_dest = module.config.log_dest
    if log_dest is not None and not log_dest.is_dir():
        log_dest.mkdir()

    mission_dest = module.config.mission_dest
    if mission_dest is not None and not mission_dest.is_dir():
        mission_dest.mkdir()

    result = staliro(specification, blackbox, module.options, module.optimizer)

    include_hash = module.config.mission_dest is not None or module.config.log_dest is not None
    json_objs = [_run_dict(num, run.history, include_hash) for num, run in enumerate(result.runs)]

    with open("results.json", "w") as results_file:
        json_dump(json_objs, results_file)


if __name__ == "__main__":
    px4test()
