# 烹饪助手 RAG 对话系统

基于 RAG（检索增强生成）技术的智能烹饪助手，可以回答关于烹饪技巧、食材选购、营养饮食、厨具使用等各类问题。

## 功能特性

- **智能问答**：基于知识库的 RAG 对话系统，回答烹饪相关问题
- **菜谱筛选**：按分类、难度、口味等条件筛选菜谱
- **知识全面**：涵盖 1182 道菜谱 + 80 条烹饪知识
- **美观的界面**：Three.js 粒子特效，支持主题切换
- **本地部署**：使用 Ollama 本地大模型，无需云端 API，完全免费

## 知识库内容

| 类别 | 数量 | 内容 |
|------|------|------|
| 菜谱 | 1182 | 八大菜系、家常菜、烘焙、饮品等 |
| 烹饪基础 | 20 | 火候、刀工、调味技巧、烹饪方法 |
| 食材知识 | 20 | 选购技巧、保存方法、处理技巧 |
| 营养饮食 | 20 | 食物属性、营养搭配、饮食禁忌 |
| 厨具知识 | 20 | 锅具保养、刀具使用、小家电技巧 |

## 快速启动

### 方式一：一键启动（Windows）

1. 下载并安装 Ollama: https://ollama.com/
2. 双击运行 `启动.bat`
3. 首次运行会自动安装依赖和下载模型
4. 访问 http://127.0.0.1:5000

### 方式二：命令行启动

```bash
# 1. 安装 Ollama (如果未安装)
# 访问 https://ollama.com/ 下载安装

# 2. 下载模型
ollama pull qwen2.5:7b

# 3. 安装 Python 依赖
pip install -r requirements.txt

# 4. 启动服务
python app.py
```

## 可选模型

默认使用 qwen2.5:7b（通义千问开源模型，中文效果好）。如需更换模型，编辑 `config.py`：

```python
class Config:
    OLLAMA_MODEL = 'llama3.1:8b'  # 更换为其他模型
```

推荐模型：
- `qwen2.5:7b`（推荐，中文好）
- `llama3.1:8b`
- `qwen2:7b`

## 项目结构

```
CookingAssistant/
├── app.py              # Flask 主应用
├── rag_system.py       # RAG 检索生成系统
├── recipe_filter.py    # 菜谱筛选逻辑
├── config.py           # 配置文件
├── static/
│   └── index.html      # 主页面
├── chroma_db/          # 向量数据库（已内置）
├── cooking_data_merged.json  # 合并数据
├── knowledge_*.json    # 知识文档
├── requirements.txt    # Python 依赖
├── 启动.bat           # Windows 一键启动
└── README.md          # 说明文档
```

## 技术栈

- **后端**：Flask + LangChain + ChromaDB
- **前端**：HTML5 + CSS3 + JavaScript + Three.js
- **模型**：Ollama 本地大模型（qwen2.5:7b）
- **向量数据库**：ChromaDB

## 使用示例

**询问菜谱**：
> 红烧肉怎么做？

**询问技巧**：
> 怎么给铁锅开锅？

**询问营养**：
> 痛风病人不能吃什么？

**询问选购**：
> 如何挑选新鲜的鱼？

## 系统要求

- Python 3.8+
- Windows / macOS / Linux
- Ollama 已安装
- 足够内存（8GB+推荐）

## 注意事项

- 向量数据库已预构建，无需重新构建
- 首次下载模型需要几分钟
- 模型运行速度取决于电脑配置
- 如需更新知识库，可运行 `rebuild_vector_db.py`

## License

MIT License
