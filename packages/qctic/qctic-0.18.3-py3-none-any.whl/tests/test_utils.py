import json
import time
from datetime import datetime, timedelta, timezone

import pytest
import qiskit.providers.aer.noise as noise
from qctic.utils import (QcticResultTimeoutError, qasm_qobj_to_dict,
                         wait_result, wait_result_async)
from qiskit import Aer, QuantumCircuit, execute
from qiskit.assembler import disassemble
from qiskit.providers import JobStatus
from qiskit.providers.aer.noise.noise_model import NoiseModel
from qiskit.qobj import QasmQobj
from werkzeug.wrappers import Response

_RESULT_SLEEP = 0.25


def _mock_simulator_result(job, httpserver, latency=_RESULT_SLEEP):
    circuits, _, _ = disassemble(job.qobj())
    simulator = Aer.get_backend("qasm_simulator")
    simulator_job = execute(circuits, simulator)
    simulator_result = simulator_job.result()
    url = "/jobs/{}".format(job.job_id())
    dtime_now = datetime.now(timezone.utc)
    dtime_end = dtime_now + timedelta(seconds=latency)
    tstamp_end = dtime_now.timestamp() + latency

    job_dict = {
        "job_id": job.job_id(),
        "qobj": job.qobj().to_dict(),
        "date_submit": dtime_now.isoformat(),
        "date_start": dtime_now.isoformat(),
        "status": JobStatus.RUNNING.name
    }

    def handler(req):
        job_res = {**job_dict}

        if time.time() >= tstamp_end:
            job_res.update({
                "date_end": dtime_end.isoformat(),
                "status": JobStatus.DONE.name,
                "result": simulator_result.to_dict()
            })

        return Response(json.dumps(job_res))

    httpserver.expect_request(url).respond_with_handler(handler)

    return simulator_result


def test_wait_result(job, httpserver):
    simulator_result = _mock_simulator_result(job, httpserver)
    result = wait_result(job, base_sleep=_RESULT_SLEEP)
    assert result.to_dict() == simulator_result.to_dict()


@pytest.mark.asyncio
async def test_wait_result_async(job, httpserver):
    simulator_result = _mock_simulator_result(job, httpserver)
    result = await wait_result_async(job, base_sleep=_RESULT_SLEEP)
    assert result.to_dict() == simulator_result.to_dict()


@pytest.mark.asyncio
async def test_wait_timeout(job, httpserver):
    base_sleep = 0.1
    sleep_growth = 1.0
    timeout = base_sleep
    latency = base_sleep * 20.0

    _mock_simulator_result(job, httpserver, latency=latency)

    with pytest.raises(QcticResultTimeoutError):
        await wait_result_async(
            job,
            base_sleep=base_sleep,
            timeout=timeout,
            sleep_growth=sleep_growth)


def test_qobj_dict_noise():
    simulator = Aer.get_backend("aer_simulator_statevector")

    error_1 = noise.depolarizing_error(1e-3, 1)
    error_2 = noise.depolarizing_error(1e-2, 2)
    noise_model = noise.NoiseModel()
    noise_model.add_all_qubit_quantum_error(error_1, ["u1", "u2", "u3"])
    noise_model.add_all_qubit_quantum_error(error_2, ["cx"])
    basis_gates = noise_model.basis_gates

    # Only "00" and "11" results would appear with an ideal noise model
    # "01" and "10" should appear with a noisy simulator
    circ = QuantumCircuit(2, 2)
    circ.h(0)
    circ.cx(0, 1)
    circ.measure([0, 1], [0, 1])

    shots = int(1e5)

    job_ideal = execute(circ, simulator, memory=False, shots=shots)
    assert len(job_ideal.result().get_counts().keys()) == 2

    job_noisy = execute(
        circ,
        simulator,
        memory=False,
        shots=shots,
        basis_gates=basis_gates,
        noise_model=noise_model)

    assert len(job_noisy.result().get_counts().keys()) > 2

    qobj_dict = qasm_qobj_to_dict(job_noisy.qobj())
    loaded_qobj = QasmQobj.from_dict(qobj_dict)
    loaded_circ, loaded_config, _ = disassemble(loaded_qobj)
    loaded_noise_model = NoiseModel.from_dict(loaded_config["noise_model"])
    assert not loaded_noise_model.is_ideal()

    loaded_job = execute(loaded_circ, simulator, **loaded_config)
    assert len(loaded_job.result().get_counts().keys()) > 2
