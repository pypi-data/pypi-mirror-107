import asyncio
import inspect
import warnings
from typing import Awaitable

from idem.exec.init import ExecReturn


async def _catch_async_exec_errors(hub, ctx, coro):
    try:
        return await hub.pop.loop.unwrap(coro)
    except Exception as a:
        return _format_error(hub, ctx, a)


def call(hub, ctx):
    # Catch exceptions in exec modules and return the error
    try:
        ret = ctx.func(*ctx.args, **ctx.kwargs)
        if asyncio.iscoroutine(ret):
            return _catch_async_exec_errors(hub, ctx, ret)
        return ret
    except Exception as e:
        return _format_error(hub, ctx, e)


def _create_exec_return(ret, ref: str):
    try:
        return ExecReturn(
            **ret,
            ref=ref,
        )
    except TypeError:
        # TODO For now, log a warning when exec module output doesn't conform to this format.
        #  later, remove this try/except
        warnings.warn(
            "Exec modules must return a dictionary {'result': True|False, 'comment': Any, 'ret': Any}",
            DeprecationWarning,
        )
        return ret


async def _create_exec_return_coro(ret: Awaitable, ref: str):
    return _create_exec_return(await ret, ref)


def post(hub, ctx):
    """
    Convert the dict return to an immutable namespace addressable format
    """
    ref = ctx.func.__module__
    if asyncio.iscoroutine(ctx.ret):
        return _create_exec_return_coro(ctx.ret, ref)
    else:
        return _create_exec_return(ctx.ret, ref)


def _format_error(hub, ctx, exc: Exception):
    ret_str = f"{exc.__class__.__name__}: {inspect.getfile(ctx.func)}:{ctx.func.__name__}: {exc}"
    hub.log.error(ret_str)
    return {"result": False, "ret": None, "comment": ret_str}
