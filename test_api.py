import requests
import json
import os
import config

# Configuration


def test_first_data_endpoint():
    """
    Test the /first_data endpoint with sample JSON data
    """
    url = f"{config.TPD_API_HOST}:{config.TPD_API_PORT}/first_data"
    
    # Sample JSON data
    sample_data = {
        "user_id": 12345,
        "event_type": "data_collection",
        "timestamp": "2024-01-15T10:30:00Z",
        "data": {
            "field1": "value1",
            "field2": "value2",
            "numbers": [1, 2, 3, 4, 5]
        }
    }
    
    # Headers with API key
    headers = {
        "Authorization": f"Bearer {os.getenv('TPD_API_KEY')}",
        "Content-Type": "application/json"
    }
    
    try:
        print("Sending POST request to /first_data...")
        print(f"URL: {url}")
        print(f"Data: {json.dumps(sample_data, indent=2)}")
        print("-" * 50)
        
        response = requests.post(url, json=sample_data, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Success! Data was received and logged to console.")
        else:
            print("❌ Error occurred.")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure the API server is running on localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_health_endpoint():
    """
    Test the health check endpoint
    """
    try:
        response = requests.get(f"{config.TPD_API_HOST}:{config.TPD_API_PORT}/health")
        print(f"Health check status: {response.status_code}")
        print(f"Health check response: {response.text}")
    except Exception as e:
        print(f"Health check error: {e}")

if __name__ == "__main__":
    print("Testing Data Collection API")
    print("=" * 50)
    
    # Test health endpoint first
    test_health_endpoint()
    print()
    
    # Test the main endpoint
    test_first_data_endpoint() 