# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此代码仓库中工作提供指导。

## 项目概述

**数字传承人 (The Digital Inheritor)** - 一个面向中国大学生计算机设计大赛的 AI 驱动非遗 (ICH) 工艺教学与复原系统。

项目采用 **多智能体协作 (Multi-Agent) 架构**，由一个中央协调器统筹三个专业智能体。

## 技术栈

### 前端
- **框架**: React 19 + TypeScript + Vite
- **样式**: Tailwind CSS
- **路由**: React Router DOM v7
- **计算机视觉**: MediaPipe Hands, TensorFlow.js (端侧推理)
- **开发命令**:
  ```bash
  cd frontend
  npm run dev      # 启动开发服务器
  npm run build    # 生产环境构建
  npm run lint     # 运行 ESLint
  ```

### 后端
- **框架**: FastAPI (Python)
- **数据库**: Neo4j (知识图谱)
- **AI/ML**: LangChain, MediaPipe, Stable Diffusion
- **开发命令**:
  ```bash
  cd backend
  pip install -r requirements.txt
  python run.py    # 启动 API 服务 (http://localhost:8000)
  ```

## 架构设计

### 多智能体系统
```
┌─────────────────────────────────────────────────────────┐
│                    主协调器 (Main Orchestrator)          │
│          (通过 MCP 协议进行意图识别与任务分发)            │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ Vision        │  │ Knowledge     │  │ Creative      │
│ Mentor Agent  │  │ Curator Agent │  │ Artisan Agent │
│ 视觉导师      │  │ 知识馆长      │  │ 创意艺匠      │
│ (手眼身法)    │  │ (博古通今)    │  │ (妙笔生花)    │
│ - MediaPipe   │  │ - RAG +       │  │ - SDXL +      │
│ - ST-GCN      │  │   Neo4j KG    │  │   ControlNet  │
│ - 姿态比对    │  │ - 问答系统    │  │ - LoRA 模型   │
└───────────────┘  └───────────────┘  └───────────────┘
```

### 后端结构 (`backend/`)
```
backend/
├── app/
│   ├── api/endpoints/       # API 路由
│   │   ├── vision_mentor.py     # POST /analyze-pose, GET /history
│   │   ├── knowledge_curator.py # RAG 问答，知识图谱查询
│   │   └── creative_artisan.py  # 图像生成，风格迁移
│   ├── core/config.py       # 配置 (Neo4j, LLM, SD 配置)
│   ├── db/seed.py           # 数据库种子数据
│   └── services/
│       ├── neo4j_service.py # Neo4j 连接与查询
│       └── llm_service.py   # LLM 集成
└── run.py                   # 入口文件
```

### 前端结构 (`frontend/`)
```
frontend/
├── src/
│   ├── pages/               # 路由页面组件
│   │   ├── Home.jsx             # 首页，智能体概览
│   │   ├── VisionMentor.jsx     # 手势追踪与姿态分析
│   │   ├── KnowledgeCurator.jsx # 问答界面
│   │   ├── MasterWorkshop.jsx   # 创意工作室
│   │   ├── CraftLibrary.jsx     # 非遗工艺库
│   │   └── MyPractice.jsx       # 用户学习进度面板
│   ├── components/
│   │   ├── HandTracking.jsx       # MediaPipe 集成组件
│   │   ├── Navbar.jsx
│   │   ├── Button.jsx
│   │   └── Card.jsx
│   └── assets/              # 静态资源 (非遗主题图片)
```

## API 端点

基础 URL: `/api/v1`

| 端点 | 智能体 | 说明 |
|------|--------|------|
| `/vision/analyze-pose` | 视觉导师 | POST 骨骼数据，获取反馈 |
| `/vision/history` | 视觉导师 | GET 用户练习历史 |
| `/knowledge/*` | 知识馆长 | RAG 问答，知识图谱查询 |
| `/creative/*` | 创意艺匠 | 图像生成，风格迁移 |

## 配置说明

### 后端 (`app/core/config.py`)
- `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD` - Neo4j 连接配置
- `OPENAI_API_KEY` - LLM API 密钥
- `STABLE_DIFFUSION_API_URL` - Stable Diffusion 推理服务地址

### 前端
- 使用 Tailwind CSS 自定义主题色 (墨黑、朱红、天青、茶绿、宣纸白)
- 中文字体：`font-calligraphy`(书法体), `font-xiaowei`(小薇体), `font-serif`(宋体)

## PRD 完成情况

根据 `PRD.md`，当前实现状态如下:

| 功能模块 | 状态 | 说明 |
|----------|------|------|
| 视觉导师 Agent (基础) | 🟡 部分完成 | 前端 MediaPipe 手部追踪已实现；后端 API 为占位符 |
| 知识馆长 Agent | 🔴 未开始 | Neo4j 服务已连接；RAG/LLM 集成待开发 |
| 创意艺匠 Agent | 🔴 未开始 | API 端点已定义；SD/ControlNet 集成待开发 |
| 主协调器 (MCP) | 🔴 未开始 | 协议未实现 |
| 用户档案系统 | 🟡 部分完成 | 基础结构已存在 (`MyPractice.jsx`) |
| 知识图谱 | 🟡 部分完成 | Neo4j 连接正常；需要数据填充 |

## 开发注意事项

- **CORS**: 后端开发模式允许所有来源 (`*`)
- **MediaPipe**: 使用 CDN 托管模型 (`@mediapipe/hands` via jsdelivr)
- **设计系统**: 东方美学主题，中国传统色配色方案
- **原型参考**: `prototype/` 目录下有静态 HTML 原型可供参考
