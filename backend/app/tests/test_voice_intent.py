from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
def test_intent():
    res = client.post('/api/v0/voice/intent', json={'user_id':'x','transcript':'todo'})
    assert res.status_code == 200
