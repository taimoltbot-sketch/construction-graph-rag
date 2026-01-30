# 安全性規則

## 絕對禁止

- ❌ 硬編碼 API Keys、Passwords、Tokens
- ❌ 將敏感資訊 Commit 到 Git
- ❌ 使用明文傳輸敏感資料

## 必須遵守

- ✅ 使用 `.env` 檔案管理 secrets
- ✅ 使用 GitHub Secrets（CI/CD 時）
- ✅ 資料庫連線使用環境變數
- ✅ API Keys 存放在安全的位置

## 檢查清單

在 `git push` 前：

1. [ ] 確認無 `.env` 檔案被 Commit
2. [ ] 確認無 API Key 在程式碼中
3. [ ] 執行 `git diff` 檢查變更
4. [ ] 使用 `secret-scanner` 掃描

## 敏感資料類型

| 類型 | 範例 |
|-----|------|
| API Keys | `ghp_xxx`, `sk-xxx` |
| 資料庫密碼 | `password`, `secret` |
| Tokens | `Bearer xxx` |
| 憑證 | `.pem`, `.key` |

## 處理流程

發現敏感資料外洩時：
1. **立即**撤銷該 Token/Key
2. 通知相關人員
3. 執行 `secret-scanner` 掃描
4. 記錄事件
