# Qwen3大模型AI Agent智能体模仿「人类记忆力」的秘密武器——开源动态知识图谱Graphiti

本项目将介绍基于开源动态知识图谱Graphiti，打造一套拥有“人类记忆力”的 AI Agent智能体。

![Graphiti动态知识图谱](https://mz-blog-res.oss-cn-beijing.aliyuncs.com/img/b007/knowl_graph_2-gh.gif)

本文所用的技术栈如下：

- Agent智能体记忆层：Graphiti
- Agent智能体流程编排：AutoGen 
- LLM大模型：Ollama 本地部署 Qwen 3 大模型

## 核心流程：

- 用户发起提问
- 智能体保存对话内容，并自动提取事实写入记忆
- 智能体检索相关事实并进行总结
- 利用历史和事实，生成更有深度的回复


## 基于动态知识图谱的Agent智能体记忆层Graphiti

开源项目Graphiti 用于构建并查询随时间演进的知识图谱。知识图谱是由相互关联的事实构成的网络，例如“Kendra 喜爱阿迪达斯鞋”。每个事实都是一个“三元组”，由两个实体或节点（“Kendra”、“阿迪达斯鞋”）及其关系或边（“喜爱”）表示。
  
知识图谱在信息检索领域已有广泛探索。Graphiti 的独特之处在于其能自主构建知识图谱，同时处理变化的关系并保持历史上下文。

![Graphiti应用示例](https://mz-blog-res.oss-cn-beijing.aliyuncs.com/img/b007/graphiti-graph-intro.gif)

  
Graphiti 构建动态的、具有时间感知的知识图谱，能够表示实体之间随时间演变的复杂关系。它同时处理非结构化和结构化数据，生成的图谱可通过时间、全文检索、语义及图算法等多种方法的融合进行查询。

  
借助 Graphiti，可以构建诸如以下的 LLM 应用：

-   能够从用户交互中学习的智能助手，将个人知识与来自 CRM 和计费平台等业务系统的动态数据相融合。
-   能够自主执行复杂任务的代理，通过整合多个动态源的状态变化进行推理。


Graphiti 支持销售、客户服务、医疗、金融等广泛领域的应用，为助手和代理提供长期记忆与基于状态的推理能力。

## 为何选择 Graphiti？

微软的 GraphRAG 在 RAG 文本分块的基础上，通过图表更好地建模文档集，并借助语义和图搜索技术使这一表示方式得以应用。然而，GraphRAG 并未解决核心问题：它主要针对静态文档设计，无法原生处理数据的时间维度。

  
Graphiti 自设计之初即着眼于处理持续变化的信息、混合语义与图搜索，以及规模化需求：

-   时间感知：追踪事实与关系随时间的变化，支持时间点查询。图的边包含时间元数据，以记录关系的生命周期。
-   事件处理：以离散事件形式摄入数据，保持数据来源可追溯，支持逐步提取实体与关系。
-   自定义实体类型：支持定义领域特定的实体类型，为专业应用实现更精确的知识表示。
-   混合搜索：结合语义搜索与 BM25 全文检索，并能根据与中心节点（如“Kendra”）的距离重新排序结果。
-   可扩展性：专为处理大规模数据集设计，通过并行化 LLM 调用进行批量处理，同时保持事件的时间顺序。
-   支持多种数据源：可处理非结构化文本和结构化 JSON 数据。


| 方面 | GraphRAG | Graphiti | 
| --------- | ---------- | ---------- | 
| **主要用途** | 静态文档摘要 | 动态数据管理 | 
| **数据处理** | 批处理导向 | 持续、增量更新 | 
| **知识结构** | 实体集群与社区摘要 | 情景数据、语义实体、社区 | 
| **检索方法** | 顺序 LLM 摘要 | 混合语义、关键词及基于图的搜索 | 
| **适应性** | 低 | 高 | 
| **时间处理** | 基础时间戳追踪 | 显式双时间追踪 |
| **矛盾处理** | LLM 驱动的摘要判断 | 时间边无效化 | 
| **查询延迟** | 秒至数十秒 | 通常亚秒级延迟 | 
| **自定义实体类型** | 不支持 | 支持，可定制 | 
| **扩展性** | 中等 | 高，针对大数据集优化 |



## 基于开源动态知识图谱Graphiti搭建Agent智能体

本项目基于Qwen3大模型和微软的AutoGen框架，使用Streamlit搭建了一个UI用户界面，搭建一个Agent智能体，用户可以通过自然语言与Agent智能体进行对话。

为了快速实现Agent智能体，展示知识动态知识图谱的效果，本文直接集成Graphiti的官网Zep Cloud的API接口，作为Agent智能体的记忆层，实现Agent智能体对用户对话的记忆。

因此，提前需要在Grapiti官网`https://www.getzep.com` ，注册账号，获取API Key。

当然，如果需要本地部署Graphiti，可以参考官网的安装指南 `https://docs.getzep.com/docs/installation/installation`。


加入博主的知识星球**AI训驼师**，将本文涉及的代码从github克隆到本地。

## 基于Ollama本地部署Qwen3大模型

### **第一步：安装Ollama**
打开终端，运行以下命令一键安装Ollama：

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

> 💡 **提示**：如果遇到权限问题，可以尝试在命令前加上`sudo`。

### **第二步：拉取Qwen3模型**
安装完成后，使用以下命令拉取Qwen3 4B模型：

```bash
ollama pull qwen3:4b
```

> ⏳ **等待时间**：根据网络情况，模型下载可能需要几分钟到几十分钟。

### **第三步：验证安装**
运行以下命令，检查Ollama是否安装成功：

```bash
ollama list
```

如果看到`qwen3:4b`出现在列表中，说明安装成功！


```python
# Ollama 模型配置
config_list = [
    {
        "model": "qwen3:4b",  # 确保上一步骤拉取的模型已经存在
        "api_type": "ollama",
        "client_host": "http://127.0.0.1:11434",  # Ollama本地部署地址
    }
]
```

## 安装项目依赖

### **第一步：安装uv**
打开终端，运行以下命令一键安装uv：

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

> 💡 **提示**：如果遇到权限问题，可以尝试在命令前加上`sudo`。

### **第二步：配置环境变量**
安装完成后，运行以下命令配置环境变量：

```bash
source $HOME/.local/bin/env
```

### **第三步：同步依赖**
使用uv同步项目依赖：

```bash
uv sync
```

### **第四步：安装Python包**
安装项目所需的Python包：

```bash
pip install zep-cloud
pip install ollama fix-busted-json
```
