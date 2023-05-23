import asyncio

from fastapi.responses import FileResponse


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
