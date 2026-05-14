# 🎯 Learning Journal

> 个人学习项目记录，持续更新中...

## 📂 项目列表

| 项目 | 描述 | 技术栈 | 状态 |
|------|------|--------|------|
| [小马逻辑](#小马逻辑) | 6×6 彩色网格逻辑推理游戏 | HTML/CSS/JS | ✅ 完成 |
| [烹饪助手](#烹饪助手) | 基于 RAG 的智能烹饪问答系统 | Flask/ChromaDB/Ollama | ✅ 完成 |

---

## 🎮 小马逻辑

一款专为心爱之人制作的逻辑推理小游戏，在 6×6 的彩色网格中找出所有小马的位置。

### 游戏规则

- 每种颜色只能放置 1 匹小马
- 每行只能放置 1 匹小马
- 每列只能放置 1 匹小马
- 小马之间不能相邻（包括斜对角方向）

### 功能特性

- 🎯 25 个关卡，逐步提升难度
- 💖 好感度系统
- ⭐ 星星收集
- ❤️ 生命机制
- 🔥 连胜记录
- 🎉 胜利动画
- 💾 本地存储存档

### 运行方式

```bash
# 直接在浏览器中打开
open game/index.html
```

### 项目结构

```
game/
├── index.html      # 游戏主页面
├── css/
│   └── style.css   # 样式文件
├── js/
│   └── game.js     # 游戏逻辑
└── README.md       # 项目说明
```

---

## 🍳 烹饪助手

基于 RAG（检索增强生成）技术的智能烹饪助手，可以回答关于烹饪技巧、食材选购、营养饮食、厨具使用等各类问题。

### 功能特性

- 💬 智能问答：基于知识库的 RAG 对话系统
- 📋 菜谱筛选：按分类、难度、口味等条件筛选
- 📚 知识全面：涵盖 1182 道菜谱 + 80 条烹饪知识
- 🎨 美观的界面：Three.js 粒子特效
- 🔒 本地部署：使用 Ollama 本地大模型，完全免费

### 快速启动

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动服务
python app.py

# 3. 访问
open http://127.0.0.1:5000
```

### 项目结构

```
CookingAssistant/
├── app.py              # Flask 主应用
├── rag_system.py       # RAG 检索生成系统
├── recipe_filter.py    # 菜谱筛选逻辑
├── config.py           # 配置文件
├── static/
│   └── index.html      # 主页面
├── chroma_db/          # 向量数据库
├── cooking_data_merged.json  # 菜谱数据
├── knowledge_*.json    # 知识文档
└── requirements.txt    # Python 依赖
```

---

## 📊 学习进度

| 时间 | 项目 | 学习内容 |
|------|------|----------|
| 2024 | 小马逻辑 | 前端基础、游戏逻辑、算法实现 |
| 2024 | 烹饪助手 | Flask 后端、RAG 架构、向量数据库、LLM 集成 |

---

## 🛠️ 技术栈

**前端**
- HTML5 / CSS3 / JavaScript
- Three.js (3D 粒子特效)

**后端**
- Python / Flask
- LangChain
- ChromaDB (向量数据库)
- Ollama (本地 LLM)

---

> 📝 每个项目都有独立的 README 文件，包含详细说明。
