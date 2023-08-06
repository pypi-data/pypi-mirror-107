# @Time     : 2021/5/28
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from asyncio import run

from f1z1_common import is_validators

from .base import ArgsType, CoroOrFunction, IRunner, IRunnerStrategy, KwargsType
from .strategy import RunStrategies, StrategyFactory


class AsyncRunner(IRunner):

    def __init__(self,
                 coro_or_func: CoroOrFunction,
                 args: ArgsType = None,
                 kwargs: KwargsType = None):
        self._coro_or_func = coro_or_func
        self._args = () if not args else args
        self._kwargs = {} if not kwargs else kwargs

    @property
    def coro_or_func(self):
        return self._coro_or_func

    @property
    def args(self):
        return self._args

    @property
    def kwargs(self):
        return self._kwargs

    def run(self):
        return run(self.main())

    async def main(self):
        runner, kwargs = self, self.kwargs
        return await self._run_impl(runner, kwargs)

    async def _run_impl(self, runner: IRunner, kwargs: KwargsType):
        coro_or_func = runner.coro_or_func
        strategy: IRunnerStrategy = None
        if self._is_coro(coro_or_func):
            strategy = StrategyFactory.create(
                RunStrategies.CORO,
                runner
            )
        elif self._is_async_function(coro_or_func):
            strategy = StrategyFactory.create(
                RunStrategies.CORO_FUNCTION,
                runner,
                kwargs=kwargs
            )
        elif self._is_function(coro_or_func):
            strategy = StrategyFactory.create(
                RunStrategies.FUNCTION,
                runner
            )
        else:
            raise ValueError(
                f"coro_or_func need coroutine, async function or function, bu got {type(coro_or_func).__name__}"
            )
        return await strategy.async_run()

    def _is_coro(self, coro_or_func: CoroOrFunction):
        return is_validators.is_coroutine(coro_or_func)

    def _is_async_function(self, coro_or_func: CoroOrFunction):
        return is_validators.is_async_function(coro_or_func)

    def _is_function(self, coro_or_func: CoroOrFunction):
        return is_validators.is_function(coro_or_func)
