# Krino Matrix

**English** | [简体中文](README.zh-CN.md)

Krino Matrix aims to free up human cognitive resources.

By using AI to understand complex states, generate feasible options, and evaluate the value of actions, we reduce the cognitive burden of processing information, analyzing, and making decisions — so everyone can devote their limited attention to more creative and meaningful work.

## Core Concepts

### Basic Elements

| Element | Description |
| --- | --- |
| `State` | The current situation |
| `Action` | A single candidate action |
| `ActionSpace` | The set of candidate actions |
| `Decision` | The chosen action and its score |

### Core Modules

| Module | Input → Output | Role |
| --- | --- | --- |
| Action Generator | `State` + objective + constraints → `ActionSpace` | Generates candidate actions |
| Action Evaluator | `State` + objective + `Action` → score | Evaluates the value of an action |

## License

[Apache License 2.0](LICENSE)
