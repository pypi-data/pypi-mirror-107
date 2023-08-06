import base64
import datetime
import json
import logging
import sys
import warnings
import zlib

from marshmallow import (INCLUDE, Schema, ValidationError, fields, post_load,
                         pre_dump, validate, validates_schema)
from qiskit.providers import JobStatus
from qiskit.qobj import QasmQobj as Qobj
from qiskit.result import Result

_WARNING_RESULT_KB_THRESHOLD = 16 * 1024.0

_MSG_RESULT_SIZE_WARNING = (
    "The size of the deserialized job result is significantly large. "
    "Please note that operations that are usually instantaneous "
    "may take a noticeable amount of time."
)

_logger = logging.getLogger(__name__)


class ResultSizeWarning(UserWarning):
    pass


def _qiskit_model_validator(klass):
    def validator(val):
        try:
            klass.from_dict(val)
            return True
        except:
            return False

    return validator


def _validate_result(val):
    if isinstance(val, str):
        return True

    return _qiskit_model_validator(Result)(val)


class GetJobsQuerySchema(Schema):
    class Meta:
        unknown = INCLUDE

    lean = fields.Boolean(required=False)

    limit = fields.Integer(
        default=10,
        required=True,
        validate=validate.Range(min=1, max=500))

    skip = fields.Integer(
        default=0,
        required=True,
        validate=validate.Range(min=0))

    status = fields.List(fields.Str(
        required=False,
        validate=validate.OneOf([item.name for item in JobStatus])))

    date_start = fields.DateTime(format="iso")
    date_end = fields.DateTime(format="iso")

    @validates_schema
    def validate_dtimes(self, data, **_):
        start = data.get("start_dtime")
        end = data.get("end_dtime")

        if start and end and end <= start:
            raise ValidationError("end_dtime must be greater than start_dtime")

    @pre_dump
    def str_status_to_list(self, data, **_):
        if isinstance(data.get("status", None), str):
            data["status"] = [data["status"]]

        return data

    @pre_dump
    def pop_falsy_lean(self, data, **_):
        if not data.get("lean"):
            data.pop("lean", None)

        return data


class JobSchema(Schema):
    class Meta:
        unknown = INCLUDE

    job_id = fields.Str(required=True)

    date_submit = fields.AwareDateTime(
        required=True,
        format="iso",
        default_timezone=datetime.timezone.utc)

    date_queue = fields.AwareDateTime(
        format="iso",
        default_timezone=datetime.timezone.utc)

    date_start = fields.AwareDateTime(
        format="iso",
        default_timezone=datetime.timezone.utc)

    date_end = fields.AwareDateTime(
        format="iso",
        default_timezone=datetime.timezone.utc)

    date_execute_start = fields.AwareDateTime(
        format="iso",
        default_timezone=datetime.timezone.utc)

    date_execute_end = fields.AwareDateTime(
        format="iso",
        default_timezone=datetime.timezone.utc)

    qobj = fields.Mapping(
        required=True,
        validate=_qiskit_model_validator(Qobj))

    status = fields.Str(
        required=True,
        validate=validate.OneOf([item.name for item in JobStatus]))

    result = fields.Raw(
        required=False,
        validate=_validate_result,
        allow_none=True)

    error = fields.Str()
    run_params = fields.Mapping()

    @post_load
    def ensure_result_dict(self, data, **_):
        result_raw = data.get("result")

        if not result_raw:
            return data

        if isinstance(result_raw, dict):
            _logger.debug("Result already a dict: No deserialization needed")
            return data

        assert isinstance(result_raw, str), f"Expected result to be a {str}"

        result_gzip = base64.b64decode(result_raw.encode())
        size_result_raw = sys.getsizeof(result_raw) / 1024.0
        size_result_gzip = sys.getsizeof(result_gzip) / 1024.0

        _logger.debug(
            "Decoded base64 raw result (%s KB) to GZIP bytes (%s KB)",
            round(size_result_raw, 1),
            round(size_result_gzip, 1))

        _logger.info("Decompressing result GZIP bytes")

        result_json_bytes = zlib.decompress(result_gzip)
        size_result_json_bytes = sys.getsizeof(result_json_bytes) / 1024.0

        _logger.debug(
            "Decompressed GZIP bytes (%s KB) to JSON bytes (%s KB)",
            round(size_result_gzip, 1),
            round(size_result_json_bytes, 1))

        if size_result_json_bytes > _WARNING_RESULT_KB_THRESHOLD:
            warnings.warn(_MSG_RESULT_SIZE_WARNING, ResultSizeWarning)

        result_dict = json.loads(result_json_bytes.decode("utf8"))

        data.update({
            "result": result_dict
        })

        return data


class BackendStatusSchema(Schema):
    class Meta:
        unknown = INCLUDE

    operational = fields.Boolean(required=True)
    pending_jobs = fields.Integer(required=True)
