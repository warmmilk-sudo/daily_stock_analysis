# -*- coding: utf-8 -*-
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.security import (
    create_access_token,
    decrypt_password,
    get_public_key,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from src.services.task_service import get_auth_service, AuthService

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    encrypted_password: str  # 前端 RSA 加密后的密码

class Token(BaseModel):
    access_token: str
    token_type: str

class PublicKeyResponse(BaseModel):
    public_key: str

@router.get("/public-key", response_model=PublicKeyResponse, summary="获取 RSA 公钥")
async def get_rsa_public_key() -> Any:
    """
    获取 RSA 公钥用于前端加密密码
    """
    return {"public_key": get_public_key()}

@router.post("/login", response_model=Token, summary="用户登录")
async def login(
    form_data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
) -> Any:
    """
    用户登录接口
    
    1. 接收 RSA 加密的密码
    2. 后端解密
    3. 验证用户名/密码
    4. 返回 JWT 令牌
    """
    try:
        # 1. 解密密码
        password = decrypt_password(form_data.encrypted_password)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="密码解密失败，请刷新页面重试",
        )
    
    # 2. 验证凭据
    if not auth_service.validate(form_data.username, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. 生成 Token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
