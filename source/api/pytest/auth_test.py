import os
import pytest

from main import app
from fastapi.testclient import TestClient

headers={"X-API-Key":os.getenv("APIKey","1234")}


# @pytest.fixture(autouse=True)
# def mock_online_validate(mocker):
#     mocker.patch('fastapi2_test.my_result', return_value="abc")


def test_auth_without_token():
    client = TestClient(app)
    response = client.get("/pets")
    assert response.status_code == 403
    assert response.json() == {'detail': 'Not authenticated'}


def test_auth_with_token():
    client = TestClient(app)
    response = client.get("/pets",headers=headers)
    assert response.status_code == 200
    assert response.json() == [{"name":"cat","description":"","id":1}]
