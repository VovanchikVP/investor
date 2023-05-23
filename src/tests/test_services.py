import asyncio
import json
import os
import pathlib

from fastapi.responses import FileResponse

from src.app.api.schemes import (
    BaseReportSchema,
    JsReportsDeclarationSchema,
)
from src.app.services.transformation_data import Transformation


def get_data_for_tests() -> Transformation:
    path = os.path.join(pathlib.Path(__file__).absolute().parents[2], pathlib.Path("temp/test_data.json"))
    with open(path) as f:
        json_data = json.load(f)
    obj = BaseReportSchema(**json_data)
    host = "localhost"
    return Transformation(host, obj)


def test_get_reports():
    loop = asyncio.get_event_loop()
    transformation = get_data_for_tests()
    coroutine = transformation.get_reports()
    response = loop.run_until_complete(coroutine)
    assert isinstance(response, FileResponse), "test failed"


def test_transformation():
    loop = asyncio.get_event_loop()
    transformation = get_data_for_tests()
    coroutine = transformation.transformation()
    data = loop.run_until_complete(coroutine)
    assert isinstance(data, JsReportsDeclarationSchema), "test failed"
