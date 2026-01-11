from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

resp = client.post('/api/v1/example/', json={'title':'Test Item','description':'An example'})
print('status:', resp.status_code)
try:
    print('json:', resp.json())
except Exception as e:
    print('text:', resp.text)
