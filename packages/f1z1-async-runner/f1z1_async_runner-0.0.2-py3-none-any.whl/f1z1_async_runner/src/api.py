# @Time     : 2021/5/28
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from asyncio import set_event_loop_policy, AbstractEventLoopPolicy
from .base import ArgsType, CoroOrFunction, KwargsType, IRunner
from .arunner import AsyncRunner


def set_loop_policy(policy: AbstractEventLoopPolicy = None):
    if policy is None:
        return
    try:
        set_event_loop_policy(policy)
    except Exception as e:
        raise e


def is_runner(value):
    return isinstance(value, IRunner)


def create_runner(
        coro_or_func: CoroOrFunction,
        args: ArgsType = None,
        kwargs: KwargsType = None
):
    return AsyncRunner(
        coro_or_func,
        args=args,
        kwargs=kwargs
    )


def start(runner: IRunner):
    if not is_runner(runner):
        raise ValueError(f"runner need IRunner instance, but got {type(runner).__name__}")
    return runner.run()
