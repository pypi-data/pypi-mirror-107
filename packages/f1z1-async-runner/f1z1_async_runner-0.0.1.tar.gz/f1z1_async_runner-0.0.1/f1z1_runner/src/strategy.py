# @Time     : 2021/5/28
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from asyncio import get_event_loop, get_running_loop
from enum import Enum
from functools import partial

from f1z1_common import is_validators

from .base import KwargsType, IRunner, IRunnerStrategy


class CoroStrategy(IRunnerStrategy):
    """
    协程对象策略
    """

    def __init__(self, runner: IRunner):
        self._runner = runner

    @property
    def runner(self):
        return self._runner

    async def execute(self, runner: IRunner, **kwargs):
        return await runner.coro_or_func

    async def async_run(self, *args, **kwargs):
        return await self.execute(runner=self.runner)


class CoroFunctionStrategy(IRunnerStrategy):
    """
    协程函数策略
    """

    def __init__(self, runner: IRunner,
                 kwargs: KwargsType = None):
        self._runner = runner
        self._kwargs = kwargs if kwargs else {}

    @property
    def runner(self):
        return self._runner

    @property
    def kwargs(self):
        return self._kwargs

    def _check_coro_function(self, value) -> bool:
        pass

    async def execute(self, runner: IRunner, **kwargs):
        return await runner.coro_or_func(*runner.args, **kwargs)

    async def async_run(self, *args, **kwargs):
        return await self.execute(
            self.runner,
            **self.kwargs
        )


class FunctionStrategy(IRunnerStrategy):

    def __init__(self, runner: IRunner):
        self._runner = runner

    @property
    def runner(self):
        return self._runner

    async def execute(self, runner: IRunner, *args, **kwargs):
        loop = get_running_loop()
        if loop is None:
            loop = get_event_loop()
        return await  loop.run_in_executor(None, runner.coro_or_func, *runner.args)

    async def async_run(self, *args, **kwargs):
        return await self.execute(self.runner)


class RunStrategies(Enum):
    CORO = CoroStrategy
    CORO_FUNCTION = CoroFunctionStrategy
    FUNCTION = FunctionStrategy


class StrategyFactory(object):

    @classmethod
    def create(cls,
               strategies: RunStrategies,
               runner: IRunner,
               **kwargs) -> IRunnerStrategy:
        klass = cls._to_subclass(strategies)
        f = cls._factory(klass, runner)
        return f(**kwargs)

    @classmethod
    def _factory(cls, subclass: IRunnerStrategy, runner: IRunner):
        if not cls._is_strategy_subclass(subclass):
            raise ValueError(f"need a IRunnerStrategy subclass, but got {type(subclass).__name__}")
        return partial(subclass, runner)

    @staticmethod
    def _is_strategy_subclass(klass):
        return issubclass(klass, IRunnerStrategy)

    @staticmethod
    def _to_subclass(strategies: RunStrategies):
        if not is_validators.is_enum(strategies):
            raise ValueError(f"strategies need Enum instance, but got {type(strategies).__name__}")
        return strategies.value
