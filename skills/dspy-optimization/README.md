# DSPy Optimization

## 為什麼用 DSPy？

- Prompt 最佳化
- 可重複使用的模組
- 自動化的 Prompt 改進
- 減少人工調參

## 核心元件

### 1. Signature

```python
import dspy

class GenerateCypher(dspy.Signature):
    """從自然語言生成 Cypher 查詢"""
    question: str = dspy.InputField()
    schema: str = dspy.InputField()
    cypher: str = dspy.OutputField()

class GenerateAnswer(dspy.Signature):
    """根據圖譜結果生成回答"""
    question: str = dspy.InputField()
    graph_context: str = dspy.InputField()
    answer: str = dspy.OutputField()
    sources: list = dspy.OutputField()
```

### 2. Module

```python
class GraphRAGModule(dspy.Module):
    def __init__(self):
        self.generate_cypher = dspy.ChainOfThought(GenerateCypher)
        self.generate_answer = dspy.ChainOfThought(GenerateAnswer)
    
    def forward(self, question: str, schema: str):
        cypher = self.generate_cypher(question=question, schema=schema)
        results = neo4j_query(cyher.cypher)
        answer = self.generate_answer(
            question=question, 
            graph_context=str(results)
        )
        return answer
```

### 3. Optimizer

```python
from dspy import evaluate

# 使用 Teleprompter 優化
teleprompter = dspy.Teleprompter(
    dspy.ChainOfThought,
    instructions="生成清晰、正確的 Cypher 查詢"
)

optimized_module = teleprompter.compile(
    GraphRAGModule(),
    trainset=training_data,
    valset=validation_data
)
```

## 使用流程

```python
# 1. 定義問題
questions = [
    "B1樓層的進度如何？",
    "鋼筋作業用了多少材料？",
    "建案目前的資金流量？"
]

# 2. 收集訓練資料
training_data = []
for q in questions:
    result = rag_pipeline.query(q)
    training_data.append({
        "question": q,
        "answeranswer,
        "": result.sources": result.sources
    })

# 3. 優化
optimized_rag = optimize_rag_pipeline(training_data)

# 4. 評估
score = evaluate(optimized_rag, test_data)
```

## 最佳實踐

1. **小步快跑**：先優化核心功能
2. **收集回饋**：持續收集使用者問題
3. **迭代改進**：定期重新訓練
4. **監控品質**：使用 LangSmith 追蹤
