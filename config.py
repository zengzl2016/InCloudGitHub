"""
配置文件 - InCloud GitHub 云上扫描器
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# GitHub配置
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')

# 扫描配置
SCAN_INTERVAL_HOURS = int(os.getenv('SCAN_INTERVAL_HOURS', 24))
OUTPUT_DIR = os.getenv('OUTPUT_DIR', './scan_reports')

# AI相关的敏感信息模式
SENSITIVE_PATTERNS = [
    # OpenAI API密钥
    r'sk-[a-zA-Z0-9]{32,}',
    r'sk-proj-[a-zA-Z0-9_-]{32,}',
    
    # Anthropic API密钥
    r'sk-ant-[a-zA-Z0-9_-]{32,}',
    
    # 环境变量模式
    r'AI_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'ANTHROPIC_AUTH_TOKEN[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'ANTHROPIC_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'OPENAI_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'CLAUDE_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # API密钥的通用模式
    r'apiKey[\s]*:[\s]*["\']([a-zA-Z0-9_-]{20,})["\']',
    r'api_key[\s]*=[\s]*["\']([a-zA-Z0-9_-]{20,})["\']',
]

# GitHub搜索关键词
AI_SEARCH_KEYWORDS = [
    'openai api',
    'anthropic claude',
    'gpt api',
    'AI_API_KEY',
    'ANTHROPIC_AUTH_TOKEN',
    'sk-ant-',
    'sk-proj-',
]

# 要排除的文件扩展名
EXCLUDED_EXTENSIONS = [
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg',
    '.mp4', '.avi', '.mov', '.wmv',
    '.zip', '.tar', '.gz', '.rar',
    '.exe', '.dll', '.so', '.dylib',
    '.pdf', '.doc', '.docx',
]

# 要排除的目录
EXCLUDED_DIRS = [
    'node_modules',
    '.git',
    'dist',
    'build',
    '__pycache__',
    'venv',
    'env',
]

# GitHub API速率限制
MAX_REPOS_PER_SEARCH = 100
SEARCH_DELAY_SECONDS = 2
