import asyncio
import copy
import logging
import uuid
import warnings

from qiskit.compiler import assemble
from qiskit.providers import BackendV1 as Backend
from qiskit.providers.aer.backends import (AerSimulator, QasmSimulator,
                                           StatevectorSimulator,
                                           UnitarySimulator)
from qiskit.providers.models import BackendConfiguration, BackendStatus
from qiskit.qobj import PulseQobj, QasmQobj

from qctic.__version__ import __version__
from qctic.job import QCticJob

_logger = logging.getLogger(__name__)


class BaseQCticSimulator(Backend):
    """Base class for CTIC Erwin simulator backends."""

    N_QUBITS = 32

    BASE_DESCRIPTION = (
        "A remote quantum simulator that acts as a proxy to Aer {} "
        "and runs on the high-performance computing platform codenamed Erwin "
        "(located at CTIC Technological Center in Gijon, Spain)"
    )

    BASE_CONFIGURATION = {
        "backend_version": __version__,
        "n_qubits": N_QUBITS,
        "url": "https://bitbucket.org/fundacionctic/erwin-qiskit",
        "local": False,
        "max_experiments": 1
    }

    _WARN_MSG_BACKEND_OPTIONS = (
        "Qiskit has deprecated the usage of backend_options. "
        "Please pass each option as an optional parameter instead."
    )

    _WARN_MSG_QOBJ = (
        "Passing instances of QasmQobj|PulseQobj to run() is deprecated."
    )

    _STATUS_OK = (
        "The QUTE quantum simulation platform is operational"
    )

    _STATUS_ERR = (
        "The QUTE quantum simulation platform is not currently operational"
    )

    def __init__(self, *args, **kwargs):
        """Constructor."""

        kwargs.update({"configuration": self.BACKEND_CONFIG})
        super().__init__(*args, **kwargs)

    @property
    def api(self):
        """QCticAPI: The API instance of this backend's provider."""

        return self.provider().api

    def _res_to_job(self, res):
        # ToDo: Should also handle serialized PulseQobj instances
        return QCticJob(
            backend=self,
            job_id=res["job_id"],
            qobj=QasmQobj.from_dict(res["qobj"]),
            remote_job=res)

    def _default_backend_status(self):
        return BackendStatus(
            backend_name=self.name(),
            backend_version=self.configuration().backend_version,
            operational=False,
            pending_jobs=0,
            status_msg=self._STATUS_ERR)

    def _res_to_backend_status(self, res):
        operational = res.get("operational")

        return BackendStatus(
            backend_name=self.name(),
            backend_version=self.configuration().backend_version,
            operational=operational,
            pending_jobs=res.get("pending_jobs"),
            status_msg=self._STATUS_OK if operational else self._STATUS_ERR)

    def _log_status_ex(self, ex):
        _logger.warning("Error fetching status: {}".format(ex))

    def run(self, run_input, **kwargs):
        """Run a set of circuits or a Qobj (deprecated) in the backend."""

        backend_options = kwargs.get("backend_options", None)

        if backend_options:
            _logger.warning(self._WARN_MSG_BACKEND_OPTIONS)
            warnings.warn(self._WARN_MSG_BACKEND_OPTIONS, DeprecationWarning)

        if isinstance(run_input, QasmQobj):
            _logger.warning(self._WARN_MSG_QOBJ)
            warnings.warn(self._WARN_MSG_QOBJ, DeprecationWarning)
            qobj = run_input
        elif isinstance(run_input, PulseQobj):
            raise ValueError(f"{PulseQobj.__name__} is not supported")
        else:
            qobj = assemble(experiments=run_input, backend=self)

        self._add_options_to_qobj(
            qobj, backend_options=backend_options, **kwargs)

        is_async = bool(kwargs.pop("async_submit", False))

        job_id = str(uuid.uuid4())
        job = QCticJob(self, job_id, qobj, run_params=kwargs)

        if is_async:
            _logger.debug("Asynchronous job submit: %s", job_id)
            job.submit_task = asyncio.ensure_future(job.submit_async())
        else:
            _logger.debug("Synchronous job submit: %s", job_id)
            job.submit()

        return job

    def _add_options_to_qobj(self, qobj, backend_options=None, **run_options):
        """Utility method to inject options into a Qobj. 
        Copied from qiskit.providers.aer.backends.aerbackend.AerBackend"""

        # Add options to qobj config overriding any existing fields
        config = qobj.config

        # Add options from the current backend instance
        for key, val in self.options.__dict__.items():
            if val is not None and not hasattr(config, key):
                setattr(config, key, val)

        # Add options indicated in a backend_options dict (deprecated)
        if backend_options is not None:
            for key, val in backend_options.items():
                setattr(config, key, val)

        # Add runtime options passed as kwargs of run()
        for key, val in run_options.items():
            setattr(config, key, val)

        return qobj

    def status(self):
        """Fetch the current status of the simulation platform.

        Returns:
            BackendStatus: The status.
        """

        try:
            res = self.api.get_backend_status_sync()
            return self._res_to_backend_status(res)
        except Exception as ex:
            self._log_status_ex(ex)
            return self._default_backend_status()

    def jobs(self, **kwargs):
        """Fetch a set of jobs that match the given filters.

        The filters can be passed as optional keyword arguments 
        that match those of the ``QCticAPI.get_jobs`` method.

        Returns:
            list(QCticJob): List of jobs.
        """

        res = self.api.get_jobs_sync(**kwargs)
        return [self._res_to_job(item) for item in res]

    def retrieve_job(self, job_id):
        """Fetch a job given its ID.

        Args:
            job_id (str): Job ID.

        Returns:
            QCticJob: The job.
        """

        job_res = self.api.get_job_sync(job_id)
        return self._res_to_job(job_res)

    async def status_async(self):
        """Asynchronous version of the ``status`` method."""

        try:
            res = await self.api.get_backend_status()
            return self._res_to_backend_status(res)
        except Exception as ex:
            self._log_status_ex(ex)
            return self._default_backend_status()

    async def jobs_async(self, **kwargs):
        """Asynchronous version of the ``jobs`` method."""

        res = await self.api.get_jobs(**kwargs)
        return [self._res_to_job(item) for item in res]

    async def retrieve_job_async(self, job_id):
        """Asynchronous version of the ``retrieve_job`` method."""

        res = await self.api.get_job(job_id)
        return self._res_to_job(res)

    def __repr__(self):
        parts = [super().__repr__()]

        try:
            method = self.options.method
            assert method
            parts.append(f"(method={method})")
        except:
            pass

        try:
            device = self.options.device
            assert device
            parts.append(f"(device={device})")
        except:
            pass

        return " ".join(parts)


def _build_configuration(name, base_cls):
    conf = copy.deepcopy(base_cls().configuration().to_dict())
    conf.update(BaseQCticSimulator.BASE_CONFIGURATION)
    description = BaseQCticSimulator.BASE_DESCRIPTION.format(base_cls.__name__)

    conf.update({
        "backend_name": name,
        "description": description
    })

    return BackendConfiguration.from_dict(conf)


class QCticQasmSimulator(BaseQCticSimulator):
    """Backend that acts as a proxy for QasmSimulator."""

    NAME = "ctic_erwin_qasm_simulator"
    BACKEND_CONFIG = _build_configuration(NAME, QasmSimulator)

    @classmethod
    def _default_options(cls):
        return QasmSimulator._default_options()


class QCticStatevectorSimulator(BaseQCticSimulator):
    """Backend that acts as a proxy for StatevectorSimulator."""

    NAME = "ctic_erwin_statevector_simulator"
    BACKEND_CONFIG = _build_configuration(NAME, StatevectorSimulator)

    @classmethod
    def _default_options(cls):
        return StatevectorSimulator._default_options()


class QCticUnitarySimulator(BaseQCticSimulator):
    """Backend that acts as a proxy for UnitarySimulator."""

    NAME = "ctic_erwin_unitary_simulator"
    BACKEND_CONFIG = _build_configuration(NAME, UnitarySimulator)

    @classmethod
    def _default_options(cls):
        return UnitarySimulator._default_options()


class QCticAerSimulator(BaseQCticSimulator):
    """Backend that acts as a proxy for AerSimulator."""

    NAME = "ctic_erwin_aer_simulator"
    BACKEND_CONFIG = _build_configuration(NAME, AerSimulator)

    @classmethod
    def _default_options(cls):
        return AerSimulator._default_options()


# ToDo: Add a proxy backend for PulseSimulator
