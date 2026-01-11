#!/usr/bin/env python3
"""
Test script for BTEC Assessment Engine FastAPI backend
"""

import requests
import pytest
import json

BASE_URL = "http://localhost:10000"

def run_health():
    """Health check helper (not a pytest test)."""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
    except requests.exceptions.RequestException:
        pytest.skip("External API not running on localhost:10000")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print()

def run_register():
    """User registration helper (not a pytest test)."""
    print("📝 Testing user registration...")
    data = {
        "email": "test@example.com",
        "password": "test123456",
        "role": "student"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
    except requests.exceptions.RequestException:
        pytest.skip("External API not running on localhost:10000")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print()
    return response.json()

def run_login(email, password):
    """User login helper (not a pytest test)."""
    print("🔐 Testing user login...")
    data = {
        "email": email,
        "password": password
    }
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
    except requests.exceptions.RequestException:
        pytest.skip("External API not running on localhost:10000")
    print(f"   Status: {response.status_code}")
    result = response.json()
    print(f"   Response: {json.dumps(result, indent=2)}")
    print()
    return result

def run_get_me(access_token):
    """Get current user info helper (not a pytest test)."""
    print("👤 Testing /me endpoint...")
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
    except requests.exceptions.RequestException:
        pytest.skip("External API not running on localhost:10000")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print()

if __name__ == "__main__":
    print("=" * 50)
    print("BTEC Assessment Engine - API Tests")
    print("=" * 50)
    print()
    
    try:
        # Test 1: Health check
        run_health()
        
        # Test 2: Register user
        try:
            user = run_register()
        except Exception as e:
            print(f"   ⚠️  Registration failed (user may already exist): {e}")
            print()
        
        # Test 3: Login
        login_result = run_login("test@example.com", "test123456")
        access_token = login_result.get("access_token")
        
        # Test 4: Get current user
        if access_token:
            run_get_me(access_token)
        
        print("=" * 50)
        print("✅ All tests completed!")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("Make sure the server is running:")
        print("  cd backend")
        print("  uvicorn app.main:app --host 0.0.0.0 --port 10000")
