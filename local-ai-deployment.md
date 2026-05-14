# 本地AI模型部署指南 - RTX 4060

## 硬件配置
- GPU: NVIDIA GeForce RTX 4060 Laptop (8GB GDDR6)
- 适合模型: 7B-13B参数规模的4-bit量化模型

## 方案一：Ollama（推荐，最简单）

### 1. 安装Ollama
```bash
# Linux安装
curl -fsSL https://ollama.com/install.sh | sh

# Windows/macOS访问: https://ollama.com/download
```

### 2. 拉取适合编程的模型
```bash
# DeepSeek-Coder V2 - 专为编程优化
ollama pull deepseek-coder:6.7b

# Qwen 2.5 Coder - 阿里的代码模型
ollama pull qwen2.5-coder:7b

# CodeLlama - Meta的代码模型
ollama pull codellama:7b-code

# Llama 3.1 - 通用模型也适合编程
ollama pull llama3.1:8b
```

### 3. 使用模型
```bash
# 直接交互
ollama run deepseek-coder:6.7b

# 或者通过API调用
curl http://localhost:11434/api/generate -d '{
  "model": "deepseek-coder:6.7b",
  "prompt": "写一个Python快速排序函数",
  "stream": false
}'
```

### 4. 常用命令
```bash
# 列出已安装模型
ollama list

# 删除模型
ollama rm <模型名>

# 查看模型信息
ollama show <模型名>
```

## 方案二：使用Python + HuggingFace（更灵活）

### 1. 安装依赖
```bash
pip install transformers torch accelerate bitsandbytes
```

### 2. 示例代码（见本地文件）

## 推荐模型列表

| 模型 | 参数 | 量化 | 显存占用 | 特点 |
|------|------|------|----------|------|
| DeepSeek-Coder-V2 | 6.7B | 4-bit | ~5GB | 编程能力强 |
| Qwen 2.5 Coder | 7B | 4-bit | ~5GB | 中文支持好 |
| CodeLlama | 7B | 4-bit | ~5GB | Meta官方 |
| Llama 3.1 | 8B | 4-bit | ~6GB | 通用能力强 |
| Mistral | 7B | 4-bit | ~5GB | 轻量高效 |

## 性能优化建议
1. 使用4-bit量化（bitsandbytes）
2. 启用Flash Attention
3. 适当调整max_new_tokens参数
