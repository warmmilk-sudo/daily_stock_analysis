# -*- coding: utf-8 -*-
"""
===================================
API v1 路由聚合
===================================

职责：
1. 聚合 v1 版本的所有 endpoint 路由
2. 统一添加 /api/v1 前缀
"""

from fastapi import APIRouter, Depends
from api.deps import get_current_user

from api.v1.endpoints import analysis, history, stocks, backtest, auth, system_config

# 创建 v1 版本主路由
router = APIRouter(prefix="/api/v1")

router.include_router(
    analysis.router,
    prefix="/analysis",
    tags=["Analysis"],
    dependencies=[Depends(get_current_user)]
)

router.include_router(
    history.router,
    prefix="/history",
    tags=["History"],
    dependencies=[Depends(get_current_user)]
)

router.include_router(
    stocks.router,
    prefix="/stocks",
    tags=["Stocks"],
    dependencies=[Depends(get_current_user)]
)

router.include_router(
    backtest.router,
    prefix="/backtest",
    tags=["Backtest"],
    dependencies=[Depends(get_current_user)]
)

router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"]
)

router.include_router(
    system_config.router,
    prefix="/system",
    tags=["SystemConfig"]
)
