import copy
import datetime
import json
import random

import pytest
from qctic.backend import (QCticAerSimulator, QCticQasmSimulator,
                           QCticStatevectorSimulator, QCticUnitarySimulator)
from qctic.utils import QobjEncoder, qasm_qobj_to_dict
from qiskit import Aer, QuantumCircuit, execute
from qiskit.assembler import disassemble
from qiskit.providers import JobStatus
from qiskit.qobj import QasmQobj
from werkzeug.wrappers import Response

from tests.utils import fake_circuit

_JOB_REMOTE = {
    "status": JobStatus.DONE.name,
    "date_submit": datetime.datetime.now().isoformat()
}


def _execute_job(req, aer_backend, assert_func=None):
    data = json.loads(req.data)
    qobj = QasmQobj.from_dict(data["qobj"])
    circuits, run_config, user_qobj_header = disassemble(qobj)

    execute_kwargs = {}
    execute_kwargs.update(run_config)
    execute_kwargs.update(data.get("run_params", {}))

    if assert_func:
        assert_func(**{
            "circuits": circuits,
            "run_config": run_config,
            "user_qobj_header": user_qobj_header,
            "execute_kwargs": execute_kwargs
        })

    backend_options = execute_kwargs.pop("backend_options", {})
    execute_kwargs.update(backend_options)

    aer_job = execute(circuits[0], aer_backend, **execute_kwargs)

    return aer_job.result()


def _handler_create_job(backend_name, job_dict, assert_func=None):
    def handler(req):
        job_result = _execute_job(
            req=req,
            aer_backend=Aer.get_backend(backend_name),
            assert_func=assert_func)

        job_dict.update({"result": job_result.to_dict()})

        return Response()

    return handler


def _handler_get_job(job, job_dict):
    def handler(req):
        job_dict.update({
            "qobj": qasm_qobj_to_dict(job.qobj()),
            "job_id": job.job_id()
        })

        job_dict_wire_safe = json.loads(json.dumps(job_dict, cls=QobjEncoder))
        job_dict.update(job_dict_wire_safe)

        return Response(json.dumps(job_dict))

    return handler


def test_backend_aersim(provider, httpserver):
    shots = random.randint(10, 100)

    backend_options = {
        "precision": "double",
        "max_parallel_threads": 2
    }

    job_remote = copy.deepcopy(_JOB_REMOTE)

    def assert_func(circuits, user_qobj_header, execute_kwargs, **_):
        assert len(circuits) == 1
        assert user_qobj_header["backend_name"] == QCticAerSimulator.NAME
        assert execute_kwargs["shots"] is shots
        assert execute_kwargs["validate"] is True
        assert execute_kwargs["memory"] is True
        assert all(key in execute_kwargs for key in backend_options.keys())

    handler_post = _handler_create_job(
        backend_name="aer_simulator_statevector",
        job_dict=job_remote,
        assert_func=assert_func)

    httpserver.expect_request("/jobs").respond_with_handler(handler_post)

    assert not job_remote.get("result")

    circuit = fake_circuit()

    job_erwin = execute(
        circuit,
        provider.get_backend(QCticAerSimulator.NAME),
        shots=shots,
        validate=True,
        memory=True,
        **backend_options)

    assert job_remote["result"]

    handler_get = _handler_get_job(job=job_erwin, job_dict=job_remote)
    job_url = "/jobs/{}".format(job_erwin.job_id())
    httpserver.expect_request(job_url).respond_with_handler(handler_get)

    result = job_erwin.result()
    result_counts = result.get_counts(circuit)
    result_memory = result.get_memory(circuit)

    assert sum(result_counts.values()) == shots
    assert len(result_memory) == shots


def test_backend_qasm(provider, httpserver):
    shots = random.randint(10, 100)

    backend_options = {
        "method": "density_matrix",
        "precision": "single"
    }

    job_remote = copy.deepcopy(_JOB_REMOTE)

    def assert_func(circuits, user_qobj_header, execute_kwargs, **_):
        assert len(circuits) == 1
        assert user_qobj_header["backend_name"] == QCticQasmSimulator.NAME
        assert execute_kwargs["shots"] is shots
        assert execute_kwargs["validate"] is False
        assert execute_kwargs["memory"] is True
        assert all(key in execute_kwargs for key in backend_options.keys())

    handler_post = _handler_create_job(
        backend_name="qasm_simulator",
        job_dict=job_remote,
        assert_func=assert_func)

    httpserver.expect_request("/jobs").respond_with_handler(handler_post)

    assert not job_remote.get("result")

    circuit = fake_circuit()

    job_erwin = execute(
        circuit,
        provider.get_backend(QCticQasmSimulator.NAME),
        shots=shots,
        validate=False,
        memory=True,
        **backend_options)

    assert job_remote["result"]

    handler_get = _handler_get_job(job=job_erwin, job_dict=job_remote)
    job_url = "/jobs/{}".format(job_erwin.job_id())
    httpserver.expect_request(job_url).respond_with_handler(handler_get)

    result = job_erwin.result()
    result_counts = result.get_counts(circuit)
    result_memory = result.get_memory(circuit)

    assert sum(result_counts.values()) == shots
    assert len(result_memory) == shots


@pytest.mark.asyncio
async def test_backend_qasm_async(provider, httpserver):
    job_remote = copy.deepcopy(_JOB_REMOTE)

    handler_post = _handler_create_job(
        backend_name="qasm_simulator",
        job_dict=job_remote)

    httpserver.expect_request("/jobs").respond_with_handler(handler_post)

    assert not job_remote.get("result")

    shots = random.randint(10, 100)
    circuit = fake_circuit()

    job_erwin = execute(
        circuit,
        provider.get_backend(QCticQasmSimulator.NAME),
        shots=shots,
        async_submit=True)

    await job_erwin.submit_task

    assert job_remote["result"]

    handler_get = _handler_get_job(job=job_erwin, job_dict=job_remote)
    job_url = "/jobs/{}".format(job_erwin.job_id())
    httpserver.expect_request(job_url).respond_with_handler(handler_get)

    status = await job_erwin.status_async()
    result = await job_erwin.result_async()
    result_counts = result.get_counts(circuit)

    assert status == job_remote["status"]
    assert sum(result_counts.values()) == shots


def test_backend_statevector(provider, httpserver):
    backend_options = {
        "zero_threshold": 1e-3
    }

    job_remote = copy.deepcopy(_JOB_REMOTE)

    def assert_func(circuits, user_qobj_header, execute_kwargs, **_):
        assert len(circuits) == 1
        assert user_qobj_header["backend_name"] == QCticStatevectorSimulator.NAME
        assert all(key in execute_kwargs for key in backend_options.keys())

    handler_post = _handler_create_job(
        backend_name="statevector_simulator",
        job_dict=job_remote,
        assert_func=assert_func)

    httpserver.expect_request("/jobs").respond_with_handler(handler_post)

    assert not job_remote.get("result")

    circuit = fake_circuit()

    job_erwin = execute(
        circuit,
        provider.get_backend(QCticStatevectorSimulator.NAME),
        **backend_options)

    assert job_remote["result"]

    handler_get = _handler_get_job(job=job_erwin, job_dict=job_remote)
    job_url = "/jobs/{}".format(job_erwin.job_id())
    httpserver.expect_request(job_url).respond_with_handler(handler_get)

    result = job_erwin.result()
    result_statevector = result.get_statevector(circuit)

    assert len(result_statevector) == 4


def test_backend_unitary(provider, httpserver):
    backend_options = {
        "zero_threshold": 1e-3
    }

    job_remote = copy.deepcopy(_JOB_REMOTE)

    def assert_func(circuits, user_qobj_header, execute_kwargs, **_):
        assert len(circuits) == 1
        assert user_qobj_header["backend_name"] == QCticUnitarySimulator.NAME
        assert all(key in execute_kwargs for key in backend_options.keys())

    handler_post = _handler_create_job(
        backend_name="unitary_simulator",
        job_dict=job_remote,
        assert_func=assert_func)

    httpserver.expect_request("/jobs").respond_with_handler(handler_post)

    assert not job_remote.get("result")

    # The unitary simulator does not support measure operations
    # pylint: disable=no-member
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)

    job_erwin = execute(
        circuit,
        provider.get_backend(QCticUnitarySimulator.NAME),
        **backend_options)

    assert job_remote["result"]

    handler_get = _handler_get_job(job=job_erwin, job_dict=job_remote)
    job_url = "/jobs/{}".format(job_erwin.job_id())
    httpserver.expect_request(job_url).respond_with_handler(handler_get)

    result = job_erwin.result()
    result_unitary = result.get_unitary(circuit)

    assert result_unitary.size == 16
