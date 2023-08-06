import logging
import os

from qiskit.providers import ProviderV1 as Provider
from qiskit.providers.providerutils import filter_backends

from qctic.api import QCticAPI
from qctic.backend import (QCticAerSimulator, QCticQasmSimulator,
                           QCticStatevectorSimulator, QCticUnitarySimulator)

_logger = logging.getLogger(__name__)


class QCticProvider(Provider):
    """Provider for CTIC QUTE backends."""

    ENV_HOST = "QCTIC_HOST"
    ENV_USERNAME = "QCTIC_USERNAME"
    ENV_PASSWORD = "QCTIC_PASSWORD"
    ENV_TOKEN = "JUPYTERHUB_API_TOKEN"

    BACKEND_OPTIONS = [
        (
            "aer_simulator",
            QCticAerSimulator,
            {}
        ),
        (
            "aer_simulator_statevector",
            QCticAerSimulator,
            {"method": "statevector"}
        ),
        (
            "aer_simulator_density_matrix",
            QCticAerSimulator,
            {"method": "density_matrix"}
        ),
        (
            "aer_simulator_stabilizer",
            QCticAerSimulator,
            {"method": "stabilizer"}
        ),
        (
            "aer_simulator_matrix_product_state",
            QCticAerSimulator,
            {"method": "matrix_product_state"}
        ),
        (
            "aer_simulator_extended_stabilizer",
            QCticAerSimulator,
            {"method": "extended_stabilizer"}
        ),
        (
            "aer_simulator_unitary",
            QCticAerSimulator,
            {"method": "unitary"}
        ),
        (
            "aer_simulator_superop",
            QCticAerSimulator,
            {"method": "superop"}
        ),
        (
            "qasm_simulator",
            QCticQasmSimulator,
            {}
        ),
        (
            "statevector_simulator",
            QCticStatevectorSimulator,
            {}
        ),
        (
            "unitary_simulator",
            QCticUnitarySimulator,
            {}
        ),
        (
            QCticAerSimulator.NAME,
            QCticAerSimulator,
            {}
        ),
        (
            QCticQasmSimulator.NAME,
            QCticQasmSimulator,
            {}
        ),
        (
            QCticStatevectorSimulator.NAME,
            QCticStatevectorSimulator,
            {}
        ),
        (
            QCticUnitarySimulator.NAME,
            QCticUnitarySimulator,
            {}
        )
    ]

    def __init__(self, *args, **kwargs):
        self._api = kwargs.pop("api")

        if not self._api:
            raise Exception("Must set the api kwarg")

        super().__init__(*args, **kwargs)

    @classmethod
    def from_env(cls, *args, **kwargs):
        host = os.getenv(cls.ENV_HOST, None)
        username = os.getenv(cls.ENV_USERNAME, None)
        password = os.getenv(cls.ENV_PASSWORD, None)
        token = os.getenv(cls.ENV_TOKEN, None)

        err_msg = "Missing Erwin environment variables: {}".format({
            cls.ENV_HOST: host,
            cls.ENV_USERNAME: username,
            cls.ENV_PASSWORD: password,
            cls.ENV_TOKEN: token
        })

        if not host:
            _logger.warning(err_msg)
            raise Exception(err_msg)

        api = QCticAPI(host=host)

        if username and password:
            api.auth_basic(username, password)
        elif token:
            api.auth_token(token)
        else:
            _logger.warning(err_msg)
            raise Exception(err_msg)

        return cls(api=api, *args, **kwargs)

    @property
    def api(self):
        return self._api

    def get_backend(self, name=None, **kwargs):
        return super().get_backend(name=name, **kwargs)

    def backends(self, name=None, filters=None, **kwargs):
        backends = []

        for bname, bcls, bopts in self.BACKEND_OPTIONS:
            if name is None or bname == name:
                the_backend = bcls(provider=self)
                the_backend.set_options(**bopts)
                backends.append(the_backend)

        return filter_backends(backends, filters=filters, **kwargs)

    def __str__(self):
        return self.__class__.__name__
