"""
Test Configuration
"""

import pytest
import sys
import os

# 確保 src 目錄在 path 中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


@pytest.fixture
def sample_project():
    """範例專案資料"""
    return {
        "id": "PRJ-001",
        "name": "台北信義區豪宅",
        "status": "進行中",
        "start_date": "2024-01-01",
        "address": "台北市信義區信義路五段",
        "budget_total": 500000000,
        "budget_reserved": 480000000,
    }


@pytest.fixture
def sample_floor():
    """範例樓層資料"""
    return {
        "id": "F-B1",
        "project_id": "PRJ-001",
        "floor_name": "B1",
        "status": "完成",
        "order_num": 0,
    }


@pytest.fixture
def sample_settlement():
    """範例結算單資料"""
    return {
        "id": "SET-001",
        "task_id": "T-001",
        "amount": 2500000,
        "date": "2024-12-15",
        "status": "已核准",
        "description": "B1鋼筋綁紮",
    }
