# -*- coding: utf-8 -*-
"""
===================================
安全相关工具模块
===================================

职责：
1. RSA 密钥生成与管理
2. 密码解密（RSA）
3. JWT 令牌生成与验证
4. 密码哈希（虽主要用RSA传参，但保留哈希能力）
"""

import os
import base64
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple

from jose import jwt, JWTError
from passlib.context import CryptContext
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

logger = logging.getLogger(__name__)

# ============================================================
# 配置
# ============================================================

# 实际生产中应从环境变量获取，这里提供默认值方便开发
SECRET_KEY = os.getenv("SECRET_KEY", "dsa-secret-key-change-me-in-prod-987654321")
ALGORITHM = "HS256"
access_token_expire_minutes_str = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440") # 默认 24 小时
try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(access_token_expire_minutes_str)
except ValueError:
    ACCESS_TOKEN_EXPIRE_MINUTES = 1440

# 密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# RSA 密钥路径
KEY_DIR = os.path.join(os.getcwd(), "keys")
PRIVATE_KEY_PATH = os.path.join(KEY_DIR, "private.pem")
PUBLIC_KEY_PATH = os.path.join(KEY_DIR, "public.pem")

# ============================================================
# RSA 密钥管理
# ============================================================

def ensure_keys_exist():
    """确保 RSA 密钥对存在，不存在则生成"""
    if not os.path.exists(KEY_DIR):
        os.makedirs(KEY_DIR)
    
    if not os.path.exists(PRIVATE_KEY_PATH) or not os.path.exists(PUBLIC_KEY_PATH):
        # 生成 2048 位 RSA 密钥
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        
        with open(PRIVATE_KEY_PATH, "wb") as f:
            f.write(private_key)
        
        with open(PUBLIC_KEY_PATH, "wb") as f:
            f.write(public_key)

def get_public_key() -> str:
    """获取 RSA 公钥字符串"""
    ensure_keys_exist()
    with open(PUBLIC_KEY_PATH, "r") as f: # pem 格式是文本
        return f.read()

def decrypt_password(encrypted_password_b64: str) -> str:
    """
    使用私钥解密前端传来的加密密码
    
    Args:
        encrypted_password_b64: Base64 编码的加密字符串
        
    Returns:
        解密后的明文密码
        
    Raises:
        ValueError: 解密失败
    """
    try:
        ensure_keys_exist()
        
        # Base64 解码
        encrypted_data = base64.b64decode(encrypted_password_b64)
        
        # 读取私钥
        with open(PRIVATE_KEY_PATH, "rb") as f:
            private_key = RSA.import_key(f.read())
        
        # 使用 PKCS1_v1_5 解密
        cipher = PKCS1_v1_5.new(private_key)
        
        # sentinel 用于解密失败时返回，防止侧信道攻击（这里直接抛错方便调试，生产环境可优化）
        sentinel = object() 
        decrypted = cipher.decrypt(encrypted_data, sentinel)
        
        if decrypted is sentinel:
             raise ValueError("Decryption failed")
             
        # 解码为字符串
        return decrypted.decode("utf-8")
        
    except Exception as e:
        raise ValueError(f"Decryption error: {str(e)}")

# ============================================================
# JWT 令牌管理
# ============================================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建 JWT 访问令牌
    
    Args:
        data: 包含在 payload 中的数据（如 sub: username）
        expires_delta: 过期时间差
        
    Returns:
        JWT 字符串
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """
    验证 JWT 令牌
    
    Returns:
        Payload 字典
        
    Raises:
        JWTError: 验证失败
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload

# ============================================================
# 密码哈希（备用）
# ============================================================

def verify_password_hash(plain_password: str, hashed_password: str) -> bool:
    """验证密码哈希（备用，如果需要存储哈希密码）"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """获取密码哈希"""
    return pwd_context.hash(password)
