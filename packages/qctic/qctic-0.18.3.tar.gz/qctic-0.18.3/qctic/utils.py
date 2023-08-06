import asyncio
import json
import time

import numpy
from qiskit.providers.aer.noise import NoiseModel

_BASE_SLEEP = 1.0
_MAX_SLEEP = 30.0
_SLEEP_GROWTH = 1.2
_TIMEOUT = None


class QcticResultTimeoutError(Exception):
    pass


def _raise_if_timeout(start, timeout):
    if timeout is None:
        return

    diff = time.time() - start

    if diff >= timeout:
        raise QcticResultTimeoutError(
            "Timeout exceeded ({} secs)".format(timeout))


def wait_result(
        job, base_sleep=_BASE_SLEEP, max_sleep=_MAX_SLEEP,
        sleep_growth=_SLEEP_GROWTH, timeout=_TIMEOUT):
    sleep = base_sleep
    start = time.time()

    while True:
        res = job.result(fetch=True)

        if res:
            return res

        _raise_if_timeout(start, timeout)
        time.sleep(sleep)
        sleep = min(sleep * sleep_growth, max_sleep)


async def wait_result_async(
        job, base_sleep=_BASE_SLEEP, max_sleep=_MAX_SLEEP,
        sleep_growth=_SLEEP_GROWTH, timeout=_TIMEOUT):
    sleep = base_sleep
    start = time.time()

    while True:
        res = await job.result_async(fetch=True)

        if res:
            return res

        _raise_if_timeout(start, timeout)
        await asyncio.sleep(sleep)
        sleep = min(sleep * sleep_growth, max_sleep)


class QobjEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()

        if isinstance(obj, complex):
            return (obj.real, obj.imag)

        if isinstance(obj, NoiseModel):
            return obj.to_dict(serializable=True)

        return json.JSONEncoder.default(self, obj)


def qasm_qobj_to_dict(qobj):
    return json.loads(json.dumps(qobj.to_dict(), cls=QobjEncoder))


def ensure_serializable_dict(input_dict):
    ret = {}

    for key, val in input_dict.items():
        try:
            ret[key] = val.to_dict(serializable=True)
        except:
            ret[key] = val

    return ret
