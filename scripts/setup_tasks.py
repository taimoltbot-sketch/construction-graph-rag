"""
Construction Graph RAG 專案任務管理
- 建立任務到 Plane
- 指派給團隊成員
- 追蹤進度
"""

import requests
import json
from datetime import datetime, timedelta

PLANE_URL = "https://api.plane.so"
PLANE_API_KEY = "plane_api_c44280b09663476ba90df98b238955da"
PLANE_WORKSPACE = "marmottaibot"

headers = {
    "x-api-key": PLANE_API_KEY,
    "Content-Type": "application/json"
}

# 團隊成員對應
TEAM_MEMBERS = {
    "planner": "MarmotTaiBot",
    "ai-engineer": "AI Engineer",
    "backend-engineer": "Backend Engineer", 
    "qa-engineer": "QA Engineer",
    "code-reviewer": "Code Reviewer"
}

def create_project(name, description):
    """建立新專案"""
    url = f"{PLANE_URL}/api/v1/workspaces/{PLANE_WORKSPACE}/projects/"
    data = {
        "name": name,
        "description": description,
        "identifier": "GRC"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        project = response.json()
        print(f"✅ 建立專案: {name}")
        return project['id']
    else:
        print(f"❌ 建立專案失敗: {response.text}")
        return None

def create_issue(project_id, name, description, priority="medium", assignee=None, start_date=None, target_date=None):
    """建立任務"""
    url = f"{PLANE_URL}/api/v1/workspaces/{PLANE_WORKSPACE}/projects/{project_id}/issues/"
    data = {
        "name": name,
        "description": description,
        "priority": priority
    }
    if assignee:
        data["assignee_id"] = assignee
    if start_date:
        data["start_date"] = start_date
    if target_date:
        data["target_date"] = target_date
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        issue = response.json()
        print(f"✅ 建立任務: {name}")
        return issue['id']
    else:
        print(f"❌ 建立任務失敗: {response.text}")
        return None

def update_issue_status(project_id, issue_id, state_name):
    """更新任務狀態"""
    # 先獲取狀態 ID
    url = f"{PLANE_URL}/api/v1/workspaces/{PLANE_WORKSPACE}/projects/{project_id}/states/"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        states = response.json().get('results', [])
        for state in states:
            if state['name'].lower() == state_name.lower():
                state_id = state['id']
                # 更新任務狀態
                update_url = f"{PLANE_URL}/api/v1/workspaces/{PLANE_WORKSPACE}/projects/{project_id}/issues/{issue_id}/"
                update_data = {"state_id": state_id}
                requests.patch(update_url, headers=headers, json=update_data)
                print(f"✅ 更新任務 {issue_id} 狀態為 {state_name}")
                return True
    return False

def get_project_issues(project_id):
    """取得專案所有任務"""
    url = f"{PLANE_URL}/api/v1/workspaces/{PLANE_WORKSPACE}/projects/{project_id}/issues/"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []

# ============================================
# Construction Graph RAG 任務清單
# ============================================

TASKS = [
    # Sprint 1: 基礎建設 (3 天)
    {
        "name": "設計 Neo4j Schema（建案、預算、合約、結算單）",
        "description": "定義營建業 Graph Schema，包含 Project、Budget、Contract、Settlement、Floor、Task、Material 等節點類型",
        "priority": "1",
        "assignee": "AI Engineer",
        "start_date": "2026-01-30",
        "target_date": "2026-01-31",
        "sprint": "Sprint 1: 基礎建設"
    },
    {
        "name": "建立 ETL Pipeline（PostgreSQL → Neo4j）",
        "description": "實作 Extract-Transform-Load 流程，將 ERP 資料轉換為三元組並載入 Neo4j",
        "priority": "1",
        "assignee": "Backend Engineer",
        "start_date": "2026-01-30",
        "target_date": "2026-01-31",
        "sprint": "Sprint 1: 基礎建設"
    },
    {
        "name": "生成 Mock Data（營建業 ERP 數據）",
        "description": "建立 Mock Data 包含：統包資料、出工結算單、建案預算、樓層進度表等",
        "priority": "2",
        "assignee": "Backend Engineer",
        "start_date": "2026-01-30",
        "target_date": "2026-01-31",
        "sprint": "Sprint 1: 基礎建設"
    },

    # Sprint 2: 核心 RAG (4 天)
    {
        "name": "實作 Graph RAG Retriever",
        "description": "整合 LangChain/LlamaIndex 的 Neo4j Graph RAG Retriever，支援混合搜尋",
        "priority": "1",
        "assignee": "AI Engineer",
        "start_date": "2026-02-01",
        "target_date": "2026-02-02",
        "sprint": "Sprint 2: 核心 RAG"
    },
    {
        "name": "實作 Cypher Query 生成（DSPy）",
        "description": "使用 DSPy 將自然語言問題轉換為 Cypher 查詢",
        "priority": "1",
        "assignee": "AI Engineer",
        "start_date": "2026-02-01",
        "target_date": "2026-02-03",
        "sprint": "Sprint 2: 核心 RAG"
    },
    {
        "name": "實作 Source Attribution",
        "description": "讓每個回答標註來源（來源表/節點、記錄 ID、信心度）",
        "priority": "2",
        "assignee": "AI Engineer",
        "start_date": "2026-02-02",
        "target_date": "2026-02-03",
        "sprint": "Sprint 2: 核心 RAG"
    },

    # Sprint 3: 介面與評估 (3 天)
    {
        "name": "建立 Chat API（FastAPI）",
        "description": "建立 REST API，支援自然語言查詢、回傳 Markdown + Mermaid 圖表",
        "priority": "1",
        "assignee": "Backend Engineer",
        "start_date": "2026-02-04",
        "target_date": "2026-02-05",
        "sprint": "Sprint 3: 介面與評估"
    },
    {
        "name": "整合 Ragas 評估",
        "description": "實作 Faithfulness、Answer Relevance、Context Precision 評估",
        "priority": "2",
        "assignee": "QA Engineer",
        "start_date": "2026-02-04",
        "target_date": "2026-02-05",
        "sprint": "Sprint 3: 介面與評估"
    },
    {
        "name": "整合 LangSmith 追蹤",
        "description": "將 RAG Pipeline 接入 LangSmith，記錄每次查詢與評估結果",
        "priority": "2",
        "assignee": "QA Engineer",
        "start_date": "2026-02-05",
        "target_date": "2026-02-06",
        "sprint": "Sprint 3: 介面與評估"
    },
]

def main():
    # 建立專案
    project_id = create_project(
        name="Construction Graph RAG",
        description="營建業知識圖譜 RAG 系統，讓建案相關人員用自然語言查詢 ERP 數據"
    )
    
    if not project_id:
        print("❌ 無法建立專案，結束")
        return
    
    print(f"\n📋 專案 ID: {project_id}")
    print(f"🔗 連結: https://app.plane.so/{PLANE_WORKSPACE}/projects/{project_id}/issues\n")
    
    # 建立所有任務
    issue_ids = []
    for task in TASKS:
        issue_id = create_issue(
            project_id=project_id,
            name=task["name"],
            description=task["description"],
            priority=task["priority"],
            assignee=task.get("assignee"),
            start_date=task.get("start_date"),
            target_date=task.get("target_date")
        )
        if issue_id:
            issue_ids.append({
                "issue_id": issue_id,
                "name": task["name"],
                "assignee": task.get("assignee"),
                "sprint": task.get("sprint")
            })
    
    print(f"\n✅ 完成！建立了 {len(issue_ids)} 個任務")
    return project_id, issue_ids

if __name__ == "__main__":
    main()
