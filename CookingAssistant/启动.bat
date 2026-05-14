@echo off
chcp 65001 >nul
title 烹饪助手 RAG 系统

echo ========================================
echo       烹饪助手 RAG 对话系统
echo ========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖
echo [1/4] 检查依赖...
python -c "import flask, flask_cors, langchain, chromadb" >nul 2>&1
if errorlevel 1 (
    echo [提示] 正在安装依赖...
    pip install flask flask-cors langchain langchain-ollama langchain-text-splitters chromadb -q
)

REM 检查Ollama
echo [2/4] 检查Ollama...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo [提示] 未检测到Ollama，请先安装Ollama
    echo [提示] 下载地址: https://ollama.com/
    pause
    exit /b 1
)

REM 检查模型
echo [3/4] 检查模型...
ollama list | findstr "qwen2.5:7b" >nul 2>&1
if errorlevel 1 (
    echo [提示] 正在下载模型 qwen2.5:7b（首次需要几分钟）...
    ollama pull qwen2.5:7b
    if errorlevel 1 (
        echo [警告] 模型下载可能有问题，请手动运行: ollama pull qwen2.5:7b
    )
)

REM 启动服务
echo [4/4] 启动服务...
echo.
echo 访问地址: http://127.0.0.1:5000
echo 按 Ctrl+C 停止服务
echo.
python app.py

pause
