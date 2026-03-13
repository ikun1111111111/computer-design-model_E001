# 知识问答系统实现总结

## 已实现功能

### 后端 (FastAPI + LangChain + Neo4j + MySQL)

#### 1. 核心服务

**`app/services/llm_service.py`** - LangChain LLM 服务
- 集成 DeepSeek 模型 (`deepseek-chat`)
- 支持对话和历史记忆
- 支持追问选项生成

**`app/services/rag_service.py`** - RAG 检索增强生成服务
- 从 Neo4j 知识图谱检索相关信息
- 结合 LLM 生成回答
- 自动生成 3 个追问选项
- 支持多种检索策略：
  - 关键词匹配
  - 按类型检索（流派/历史/传承人/剧目）
  - 通用检索

**`app/db/mysql_db.py`** - MySQL 数据库模型
- `Conversation` 表：存储对话历史
- `FollowUpQuestion` 表：存储追问选项

#### 2. API 端点

**`/api/v1/knowledge/query`** (POST)
```json
// 请求
{
  "query": "皮影戏有哪些主要流派？",
  "session_id": "可选-会话 ID"
}

// 响应
{
  "answer": "AI 生成的回答",
  "follow_up_questions": ["追问 1", "追问 2", "追问 3"],
  "related_entities": ["相关实体 1", "相关实体 2"],
  "session_id": "会话 ID"
}
```

**`/api/v1/knowledge/session/{session_id}`** (GET)
- 获取会话历史

**`/api/v1/knowledge/entities`** (GET)
- 获取所有相关实体

### 前端 (React)

**`KnowledgeCurator.jsx`** - 知识馆长页面
- 聊天界面
- 追问选项按钮（可点击发送）
- 会话管理（localStorage 存储 session_id）
- 相关实体标签展示
- 知识图谱可视化（左侧面板）

### 数据库

**MySQL**
- 数据库：`inheritor_db`
- 表：`conversations`, `follow_up_questions`

**Neo4j**
- 知识图谱：皮影戏相关数据
- 节点类型：Heritage, School, Person, Drama, History, etc.

## 技术栈

| 组件 | 技术 |
|------|------|
| LLM | DeepSeek (`deepseek-chat`) |
| 框架 | LangChain |
| 知识图谱 | Neo4j |
| 数据库 | MySQL |
| 后端 | FastAPI |
| 前端 | React |

## 使用方法

### 1. 启动后端

```bash
cd backend
pip install -r requirements.txt
python app/db/init_db.py  # 初始化 MySQL 数据库
python run.py             # 启动服务器 (http://localhost:8000)
```

### 2. 启动前端

```bash
cd frontend
npm run dev  # 启动开发服务器 (http://localhost:5173)
```

### 3. 访问知识馆长

打开浏览器访问：`http://localhost:5173/knowledge-curator`

## 示例对话

### 问题 1：皮影戏的流派
```
用户：皮影戏有哪些主要流派？

AI: 根据提供的知识图谱信息，虽有提及皮影戏的定义、分类、非遗级别入选时间以及一些代表剧目和一位传承人，但信息中并未明确列出皮影戏的主要流派分类。

作为补充，我可以基于一般知识告知您：皮影戏在中国分布广泛，不同地区确实发展形成了众多地方特色流派，如陕西皮影、河北唐山皮影、浙江海宁皮影、四川皮影、山东皮影、广东陆丰皮影等，各有其独特的制作风格和唱腔特点。

如果您想了解某个特定流派皮影戏的详细信息，您可以尝试提出更具体的问题，这样我或许能为您提供更有针对性的信息。

追问选项:
- 陕西皮影有什么特点？
- 唐山皮影的唱腔属于哪种戏曲类型？
- 详细说说《五峰会》的故事内容
```

### 问题 2：历史起源
```
用户：皮影戏的历史起源

AI: [基于知识图谱数据回答]

追问选项:
- [自动生成 3 个相关问题]
```

## 注意事项

### 编码问题
Neo4j 中的中文数据可能存在编码问题，建议重新导入数据时确保：
1. JSON 文件使用 UTF-8 编码
2. Neo4j 客户端使用 UTF-8 连接
3. Python 脚本读取时使用 `encoding='utf-8'`

### API 密钥
当前使用的 DeepSeek API Key 为：`sk-ef663e51e8224d99803c7fbc6f137a86`
建议在 `.env` 文件中配置：
```
DEEPSEEK_API_KEY=your-api-key-here
```

### 数据库配置
```
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=inheritor_db
```

## 下一步优化

1. **修复编码问题**: 重新导入 Neo4j 数据，确保中文正常显示
2. **添加向量检索**: 集成 Milvus 进行语义搜索
3. **优化检索策略**: 改进 Cypher 查询，提高检索准确性
4. **添加流式响应**: 支持打字机效果输出
5. **增强对话管理**: 支持多轮对话和上下文理解
