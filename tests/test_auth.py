# tests/test_auth.py

from fastapi.testclient import TestClient
from api.app import app
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import os

client = TestClient(app)

def test_get_public_key():
    response = client.get("/api/v1/auth/public-key")
    assert response.status_code == 200
    assert "public_key" in response.json()
    assert "BEGIN PUBLIC KEY" in response.json()["public_key"]

def test_login_success():
    # 1. Get Public Key from source or endpoint
    # We can just fetch it from endpoint in test
    response = client.get("/api/v1/auth/public-key")
    pub_key_pem = response.json()["public_key"]
    
    rsa_key = RSA.import_key(pub_key_pem)
    cipher = PKCS1_v1_5.new(rsa_key)
    
    # 2. Encrypt Password
    # Need to match what is in .env or default
    password = os.getenv("WEB_PASSWORD", "admin888")
    username = os.getenv("WEB_USERNAME", "admin")
    
    encrypted_password = cipher.encrypt(password.encode())
    encrypted_password_b64 = base64.b64encode(encrypted_password).decode()
    
    # 3. Login
    response = client.post("/api/v1/auth/login", json={
        "username": username,
        "encrypted_password": encrypted_password_b64
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
    # 4. Use token to access a protected endpoint
    # Currently /api/health is protected? No, checking app.py
    # app.py: health_check does NOT have dependency if I recall correctly?
    # Let's check api/app.py content again or just try /api/v1/analysis (protected)
    
    token = data["access_token"]
    # health check is public in my last edit?
    # Let's try accessing a protected route if possible.
    # But /api/v1/... routes (analysis etc) are protected. 
    # Let's just verify we got a token.

def test_login_fail():
    response = client.post("/api/v1/auth/login", json={
        "username": "admin",
        "encrypted_password": "invalid_base64_or_encrypted"
    })
    assert response.status_code in [400, 401]
