# RAG Evaluation

## 評估框架

```
User Query → RAG Pipeline → Answer + Sources → Evaluation Metrics
```

## 評估指標

### 1. Faithfulness（忠實度）
回答是否忠於檢索到的圖譜資料。

```python
from ragas.metrics import faithfulness

score = evaluate(
    dataset,
    metrics=[faithfulness]
)
```

### 2. Answer Relevance（切題度）
回答是否切合使用者問題。

```python
from ragas.metrics import answer_relevance

score = evaluate(
    dataset,
    metrics=[answer_relevance]
)
```

### 3. Context Precision（檢索精確度）
檢索結果的相關性排序。

```python
from ragas.metrics import context_precision

score = evaluate(
    dataset,
    metrics=[context_precision]
)
```

### 4. Source Attribution（來源標註）
檢查來源標註是否正確。

```python
def source_attribution_score(result) -> float:
    """計算來源標註正確率"""
    correct = 0
    for source in result.sources:
        if verify_source(source):
            correct += 1
    return correct / len(result.sources) if result.sources else 1.0
```

## 評估資料集格式

```python
from ragas import Dataset

evaluation_data = [
    {
        "question": "B1樓層的鋼筋作業進度如何？",
        "answer": "B1鋼筋作業已完成100%，使用鋼筋100噸",
        "contexts": [
            "Task(T-001, name=鋼筋綁紮, progress=100)",
            "Material(M-001, name=鋼筋, quantity=100)"
        ],
        "ground_truth": "B1鋼筋作業100%完成，鋼筋用量100噸"
    }
]

dataset = Dataset.from_list(evaluation_data)
```

## LangSmith 整合

```python
import langsmith

@langsmith.traceable
def evaluate_rag_pipeline(question: str, answer: str, contexts: list):
    """LangSmith 可追蹤每次評估"""
    result = rag_pipeline.evaluate(
        question, answer, contexts
    )
    return result
```

## 閾值設定

| 指標 | 目標 | 最低可接受 |
|-----|------|----------|
| Faithfulness | > 0.85 | 0.80 |
| Answer Relevance | > 0.80 | 0.75 |
| Context Precision | > 0.85 | 0.80 |
| Source Attribution | > 0.90 | 0.85 |
