# /evaluate - 執行評估

## 使用方式

```
/evaluate [類型]
```

## 功能

執行 RAG 評估並生成報告

## 評估類型

| 類型 | 說明 | 命令 |
|-----|------|------|
| all | 執行所有評估 | `/evaluate` |
| rag | RAG 指標評估 | `/evaluate rag` |
| data | 資料完整性檢查 | `/evaluate data` |
| dspy | DSPy Prompt 優化 | `/evaluate dspy` |

## 評估指標

### RAG 指標
- **Faithfulness**: 回答忠於檢索內容
- **Answer Relevance**: 回答切題程度
- **Context Precision**: 檢索精確度
- **Source Attribution**: 來源標註正確性

### 資料指標
- **完整性**: 無遺漏節點
- **一致性**: 關係正確
- **正確性**: 數據無誤

## 輸出範例

```markdown
## 評估報告

### RAG 評估結果
| 指標 | 分數 | 閾值 | 狀態 |
|------|------|------|------|
| Faithfulness | 0.85 | 0.80 | ✅ |
| Answer Relevance | 0.78 | 0.80 | ⚠️ |
| Context Precision | 0.90 | 0.85 | ✅ |
| Source Attribution | 0.95 | 0.90 | ✅ |

### 建議
- Answer Relevance 低於閾值，建議優化 prompt
```
```
