import sys
import os

# Configurar el path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

print(f"Python path: {sys.path}")
print(f"Current directory: {os.getcwd()}")
print(f"Parent directory: {parent_dir}")

try:
    from fastapi.testclient import TestClient
    from main import app
    
    client = TestClient(app)

    def test_health_check():
        """Test health check endpoint"""
        try:
            response = client.get("/health")
            print(f"Response status code: {response.status_code}")
            print(f"Response body: {response.json()}")
            assert response.status_code == 200
            assert response.json() == {"status": "healthy"}
        except Exception as e:
            print(f"Error during test: {str(e)}")
            raise
except Exception as e:
    print(f"Error during imports: {str(e)}")
    raise
