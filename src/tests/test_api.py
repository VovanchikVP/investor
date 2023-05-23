import json
import os
import pathlib

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_reports():
    path = os.path.join(pathlib.Path(__file__).absolute().parents[2], pathlib.Path("temp/test_data.json"))
    with open(path) as f:
        json_data = json.load(f)
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    response = client.post("/api/v1/reports", headers=headers, json=json_data)
    assert response.status_code == 200, "test failed"
