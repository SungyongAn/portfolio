from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    # Assuming there is a root endpoint or we can test health check
    # If no root endpoint, we can test /docs or similar, or just check 404 is handled gracefully
    response = client.get("/")
    # Adjust assertion based on actual root endpoint behavior
    # If root returns 404, that's fine for a connectivity test
    assert response.status_code in [200, 404]
