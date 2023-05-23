from fastapi import (
    Depends,
    UploadFile,
)

from src.app.api.schemes import ExampleSchema
from src.app.services.example import BrokerReports


async def initial_data(file: UploadFile, data: ExampleSchema = Depends()):
    """Пример запроса данных"""
    await BrokerReports.create(file)
    print(data)
    return {"test": "test"}
