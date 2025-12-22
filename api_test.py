import requests
import json
import time

BASE_URL = "http://localhost:8000"

def log_test(name, result, time_taken=None):
    status = "✅ PASS" if result else "❌ FAIL"
    time_str = f" ({time_taken:.2f}s)" if time_taken is not None else ""
    print(f"{status} - {name}{time_str}")

def test_root():
    start = time.time()
    try:
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        data = response.json()
        log_test("Root Endpoint", True, time.time() - start)
    except Exception as e:
        print(f"Error in root: {e}")
        log_test("Root Endpoint", False)

def test_health():
    start = time.time()
    try:
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        log_test("Health Check", True, time.time() - start)
    except Exception as e:
        print(f"Error in health: {e}")
        log_test("Health Check", False)

def test_predict_get():
    start = time.time()
    try:
        response = requests.get(f"{BASE_URL}/predict")
        assert response.status_code == 200
        data = response.json()
        assert "top_numbers" in data
        assert len(data["top_numbers"]) == 15
        log_test("GET /predict (Defaults)", True, time.time() - start)
    except Exception as e:
        print(f"Error in GET /predict: {e}")
        log_test("GET /predict", False)

def test_user_predict_post():
    start = time.time()
    try:
        payload = {"top_n": 10, "n_combinations": 5}
        response = requests.post(f"{BASE_URL}/user/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert len(data["top_numbers"]) == 10
        log_test("POST /user/predict", True, time.time() - start)
    except Exception as e:
        print(f"Error in POST /user/predict: {e}")
        log_test("POST /user/predict", False)

def test_admin_retrain():
    start = time.time()
    try:
        response = requests.post(f"{BASE_URL}/admin/retrain")
        assert response.status_code == 200
        log_test("POST /admin/retrain", True, time.time() - start)
    except Exception as e:
        print(f"Error in POST /admin/retrain: {e}")
        log_test("POST /admin/retrain", False)

if __name__ == "__main__":
    print(f"Testing API at {BASE_URL}...\n")
    try:
        requests.get(BASE_URL)
        test_root()
        test_health()
        test_predict_get()
        test_user_predict_post()
        test_admin_retrain()
        print("\nAll tests completed.")
    except Exception as e:
        print(f"❌ Error: Could not connect to {BASE_URL}. Is the server running?")
