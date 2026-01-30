"""
TDD Test: ETL Pipeline
測試資料轉換功能
"""

import pytest

from src.etl.pipeline import Transformer


class TestTransformer:
    """Transformer 測試"""

    def test_project_to_triples_returns_list(self):
        """測試 project_to_triples 回傳 list"""
        project = {
            "id": "PRJ-001",
            "name": "台北豪宅",
            "status": "進行中",
            "budget_total": 500000000,
        }
        result = Transformer.project_to_triples(project)
        assert isinstance(result, list)
        assert len(result) > 0

    def test_project_to_triples_contains_id(self):
        """測試 project_to_triples 包含 id"""
        project = {"id": "PRJ-001", "name": "測試建案", "status": "進行中"}
        result = Transformer.project_to_triples(project)
        # 檢查是否包含 (Project, PRJ-001, id, PRJ-001)
        assert ("Project", "PRJ-001", "id", "PRJ-001") in result

    def test_project_to_triples_contains_name(self):
        """測試 project_to_triples 包含名稱"""
        project = {"id": "PRJ-001", "name": "測試建案", "status": "進行中"}
        result = Transformer.project_to_triples(project)
        assert ("Project", "PRJ-001", "name", "測試建案") in result

    def test_project_to_triples_contains_status(self):
        """測試 project_to_triples 包含狀態"""
        project = {"id": "PRJ-001", "name": "測試建案", "status": "進行中"}
        result = Transformer.project_to_triples(project)
        assert ("Project", "PRJ-001", "status", "進行中") in result

    def test_project_to_triples_with_budget(self):
        """測試有預算的專案轉換"""
        project = {
            "id": "PRJ-001",
            "name": "測試建案",
            "status": "進行中",
            "budget_total": 500000000,
        }
        result = Transformer.project_to_triples(project)
        assert ("Project", "PRJ-001", "budget_total", 500000000) in result

    def test_floor_to_triples(self):
        """測試樓層轉換"""
        floor = {
            "id": "F-B1",
            "floor_name": "B1",
            "status": "完成",
        }
        result = Transformer.floor_to_triples(floor)
        assert ("Floor", "F-B1", "id", "F-B1") in result
        assert ("Floor", "F-B1", "floor_name", "B1") in result
        assert ("Floor", "F-B1", "status", "完成") in result

    def test_settlement_to_triples(self):
        """測試結算單轉換"""
        settlement = {
            "id": "SET-001",
            "amount": 2500000,
            "status": "已核准",
        }
        result = Transformer.settlement_to_triples(settlement)
        assert ("Settlement", "SET-001", "id", "SET-001") in result
        assert ("Settlement", "SET-001", "amount", "2500000") in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
