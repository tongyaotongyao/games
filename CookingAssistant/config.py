import os


class Config:
    OLLAMA_BASE_URL = 'http://localhost:11434'
    OLLAMA_MODEL = 'qwen2.5:7b'
    CHROMA_DB_PATH = './chroma_db'
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 100
    TOP_K = 5
