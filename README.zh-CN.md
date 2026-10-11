# Krino Matrix

[English](README.md) | **简体中文**

Krino Matrix 致力于解放人的认知资源。

我们希望通过人工智能理解复杂状态、生成可行方案并评估行动价值，降低人们在信息处理、分析和决策上的认知负担，让每个人都能将有限的认知资源投入更有创造性、更有价值的事情中。

## 核心概念

### 基本元素

| 元素 | 说明 |
| --- | --- |
| `State` | 当前状态 |
| `Action` | 单个候选行动 |
| `ActionSpace` | 候选行动的集合 |
| `Decision` | 最终选择的行动及其得分 |

### 核心模块

| 模块 | 输入 → 输出 | 作用 |
| --- | --- | --- |
| Action Generator | `State` + 目标 + 约束 → `ActionSpace` | 生成候选行动 |
| Action Evaluator | `State` + 目标 + `Action` → 得分 | 评估行动的价值 |

## 许可证

[Apache License 2.0](LICENSE)
