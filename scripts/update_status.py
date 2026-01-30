"""更新 Plane 任務狀態"""

import requests

PLANE_URL = 'https://api.plane.so'
PLANE_API_KEY = 'plane_api_c44280b09663476ba90df98b238955da'
PLANE_WORKSPACE = 'marmottaibot'
PROJECT_ID = '8085a5b4-49cc-4777-b458-4847a95b4d4c'

headers = {
    'x-api-key': PLANE_API_KEY,
    'Content-Type': 'application/json'
}

# 狀態 ID
DONE_STATE = '097b687a-559a-4219-b235-34657468ee80'
IN_PROGRESS_STATE = '61b49a57-3c88-4cc0-905b-fd22b486997c'

# 取得所有任務
url = f'{PLANE_URL}/api/v1/workspaces/{PLANE_WORKSPACE}/projects/{PROJECT_ID}/issues/'
response = requests.get(url, headers=headers)
issues = response.json().get('results', [])

print('📋 任務狀態更新')
print('=' * 60)

completed_tasks = ['設計 Neo4j Schema', '生成 Mock Data', '建立 ETL Pipeline']

for issue in issues:
    issue_id = issue['id']
    issue_name = issue['name']
    
    is_completed = any(task in issue_name for task in completed_tasks)
    
    if is_completed:
        update_url = f'{PLANE_URL}/api/v1/workspaces/{PLANE_WORKSPACE}/projects/{PROJECT_ID}/issues/{issue_id}/'
        data = {'state_id': DONE_STATE}
        resp = requests.patch(update_url, headers=headers, json=data)
        if resp.status_code == 200:
            print(f'✅ {issue_name} -> Done')
        else:
            print(f'❌ {issue_name} failed: {resp.text[:100]}')
    else:
        update_url = f'{PLANE_URL}/api/v1/workspaces/{PLANE_WORKSPACE}/projects/{PROJECT_ID}/issues/{issue_id}/'
        data = {'state_id': IN_PROGRESS_STATE}
        resp = requests.patch(update_url, headers=headers, json=data)
        if resp.status_code == 200:
            print(f'🔄 {issue_name} -> In Progress')
        else:
            print(f'❌ {issue_name} failed')

print('=' * 60)
print('狀態更新完成！')
