import argparse
import asyncio
import logging
import pprint
import random

from qiskit import execute
from qiskit.circuit.random import random_circuit

from qctic.backend import (QCticAerSimulator, QCticQasmSimulator,
                           QCticStatevectorSimulator, QCticUnitarySimulator)
from qctic.provider import QCticProvider
from qctic.utils import wait_result_async

_MIN_QUBITS = 2
_PROB_H = 0.5

_logger = logging.getLogger("qctic")


def init_logging():
    try:
        import coloredlogs
        coloredlogs.install(level=logging.DEBUG, logger=_logger)
    except ImportError:
        _logger.setLevel(logging.DEBUG)
        logging.basicConfig()


def _rand_circuit(qubits, unitary=False, depth=3):
    qubits = max(_MIN_QUBITS, qubits)
    measure = not unitary
    circuit = random_circuit(num_qubits=qubits, depth=depth, measure=measure)
    return circuit


def build_result_msg_qasm(result, circuit):
    return "## Counts:\n{}\n## Memory:\n{}".format(
        pprint.pformat(result.get_counts(circuit)),
        pprint.pformat(result.get_memory(circuit)))


def build_result_msg_unitary(result, circuit):
    return "## Unitary:\n{}".format(
        pprint.pformat(result.get_unitary(circuit)))


def build_result_msg_statevector(result, circuit):
    return "## Statevector:\n{}".format(
        pprint.pformat(result.get_statevector(circuit)))


def log_result(result, circuits, backend_name):
    msg_funcs = {
        QCticAerSimulator: build_result_msg_qasm,
        QCticQasmSimulator: build_result_msg_qasm,
        QCticUnitarySimulator: build_result_msg_unitary,
        QCticStatevectorSimulator: build_result_msg_statevector
    }

    backend_cls = next(
        item[1] for item in QCticProvider.BACKEND_OPTIONS
        if item[0] == backend_name)

    msg_func = msg_funcs[backend_cls]

    for idx, circ in enumerate(circuits):
        _logger.info("Circuit #%s results:\n%s", idx, msg_func(result, circ))


async def execute_jobs(qubits, backend_name, num_circuits, shots, gpu):
    qctic_provider = QCticProvider.from_env()
    qctic_backend = qctic_provider.get_backend(backend_name)

    is_unitary = next((
        True for item in QCticProvider.BACKEND_OPTIONS
        if item[0] == backend_name and item[1] is QCticUnitarySimulator), False)

    circuits = [
        _rand_circuit(qubits=qubits, unitary=is_unitary)
        for _ in range(num_circuits)
    ]

    for idx, circ in enumerate(circuits):
        _logger.info("Circuit #%s:\n%s", idx, circ.draw())

    backend_options = {"device": "GPU" if gpu else "CPU"}

    memory = backend_name in [
        item[0] for item in QCticProvider.BACKEND_OPTIONS
        if item[1] in (QCticAerSimulator, QCticQasmSimulator)
    ]

    qctic_job = execute(
        circuits,
        qctic_backend,
        shots=shots,
        memory=memory,
        **backend_options)

    await qctic_job.submit_task
    result = await wait_result_async(qctic_job)

    if not result.success:
        _logger.error("Some of the experiments failed")

        for idx, exp_res in enumerate(result.results):
            _logger.warning("Circuit #%s status: %s", idx, exp_res.status)

        return

    log_result(result=result, circuits=circuits, backend_name=backend_name)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--circuits", type=int, default=1)
    parser.add_argument("--shots", type=int, default=10)
    parser.add_argument("--qubits", type=int, default=4)
    parser.add_argument("--gpu", action="store_true")

    parser.add_argument(
        "--backend",
        default=QCticQasmSimulator.NAME,
        choices=[item[0] for item in QCticProvider.BACKEND_OPTIONS])

    return parser.parse_args()


def main():
    init_logging()
    loop = asyncio.get_event_loop()
    args = parse_args()

    _logger.debug("Arguments: %s", args)

    def stop_cb(fut):
        _logger.debug("Main task: %s", fut)
        loop.stop()

    try:
        main_task = asyncio.ensure_future(execute_jobs(
            qubits=args.qubits,
            backend_name=args.backend,
            num_circuits=args.circuits,
            shots=args.shots,
            gpu=args.gpu))

        main_task.add_done_callback(stop_cb)
        loop.run_forever()
    except:
        _logger.error("Error", exc_info=True)
    finally:
        _logger.debug("Closing loop")
        loop.close()


if __name__ == "__main__":
    main()
