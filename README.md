# InCloud GitHub 云上扫描器

<div align="center">

🔍 **AI API Key Leakage Scanner**

自动扫描 GitHub 仓库，发现泄露的 AI API 密钥和敏感信息

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub Actions](https://img.shields.io/badge/automation-GitHub%20Actions-2088FF.svg)](https://github.com/features/actions)

</div>

---

## 🌟 特性

- 🤖 **GitHub Actions 自动化** - 云端定时扫描，无需本地运行
- 🔍 **智能检测** - 支持 OpenAI、Anthropic 等多种 AI API 密钥格式
- 📊 **详细报告** - 自动生成并保存扫描报告（保留 90 天）
- 🔔 **自动告警** - 发现问题时自动创建 Issue
- 🎯 **多种模式** - 支持用户/组织/单仓/自动搜索
- 💰 **完全免费** - 公开仓库无限使用 GitHub Actions

---

## 🚀 快速开始

### 第 1 步：推送到 GitHub

```bash
# 克隆或下载本项目到本地
cd ai-scan

# 初始化 Git 仓库
git init
git add .
git commit -m "feat: AI API Key Scanner"

# 在 GitHub 创建新仓库，然后关联并推送
git remote add origin https://github.com/YOUR_USERNAME/ai-scanner.git
git branch -M main
git push -u origin main
```

### 第 2 步：配置 GitHub Token

#### 2.1 获取 Personal Access Token

1. 访问：https://github.com/settings/tokens
2. 点击 **"Generate new token"** → **"Generate new token (classic)"**
3. 设置：
   - **Note**: `AI Scanner Token`
   - **Expiration**: 90 days 或更长
   - **Scopes**: 
     - ✅ `public_repo` - 访问公开仓库
     - ✅ `read:org` - 读取组织信息（可选）
4. 点击 **"Generate token"** 并复制

#### 2.2 添加到仓库 Secrets

1. 访问你的仓库设置：
   ```
   https://github.com/YOUR_USERNAME/ai-scanner/settings/secrets/actions
   ```
2. 点击 **"New repository secret"**
3. 添加 Secret：
   - **Name**: `GH_SCAN_TOKEN`
   - **Value**: 粘贴你复制的 Token
4. 点击 **"Add secret"**

### 第 3 步：运行扫描

#### 选项 A：手动触发（推荐首次测试）

1. 访问 Actions 页面：
   ```
   https://github.com/YOUR_USERNAME/ai-scanner/actions
   ```

2. 选择 **"AI API Key Scanner - Manual Scan"**

3. 点击 **"Run workflow"** 按钮

4. 填写参数：
   - **Scan type**: `auto - 自动搜索AI项目`
   - **Target**: 留空（auto 模式）
   - **Max repos**: `5` （首次测试建议小数量）
   - **Create issue**: ✅ 勾选

5. 点击 **"Run workflow"** 开始扫描

#### 选项 B：自动运行

配置完成后，**每天 UTC 02:00（北京时间 10:00）** 会自动运行扫描。

---

## 📊 查看结果

### 1. 实时查看运行日志

在 Actions 页面点击运行记录，可以看到：
- 🔍 扫描进度
- 📊 发现的问题统计
- ✅ 执行状态

### 2. 下载完整报告

1. 进入运行详情页
2. 滚动到页面底部的 **"Artifacts"** 区域
3. 下载报告文件（TXT 格式，保留 90 天）

### 3. 查看自动创建的 Issue

如果发现潜在问题，系统会自动创建 Issue：
- 🏷️ 标签：`security`, `auto-scan`
- 📋 包含问题摘要、统计信息
- 💡 提供安全建议和处理步骤

---

## ⚙️ 工作流说明

项目包含 3 个 GitHub Actions 工作流：

### 1. `auto-scan.yml` - 基础自动扫描

**功能**：
- 每天定时自动扫描 AI 相关项目
- 支持手动触发并选择扫描模式
- 自动上传报告和创建 Issue

**适用场景**：日常自动监控

---

### 2. `manual-scan.yml` - 手动扫描（推荐）

**功能**：
- 完全手动控制的扫描
- 支持 4 种扫描模式：
  - 🤖 **Auto** - 自动搜索 AI 相关项目
  - 👤 **User** - 扫描指定用户的所有仓库
  - 🏢 **Org** - 扫描指定组织的所有仓库
  - 📦 **Repo** - 扫描单个指定仓库
- 可自定义所有参数

**适用场景**：按需扫描特定目标

**使用示例**：
```
Scan type: user - 扫描指定用户
Target: openai
Max repos: 10
Create issue: true
```

---

### 3. `scheduled-scan.yml` - 增强定时扫描

**功能**：
- 详细的扫描统计和分析
- 智能 Issue 管理（同一天只创建一个 Issue）
- 生成详细的扫描摘要
- 超时保护（60 分钟）

**适用场景**：企业级定期安全审计

---

## 🎯 自定义配置

### 修改扫描时间

编辑 `.github/workflows/scheduled-scan.yml`：

```yaml
on:
  schedule:
    - cron: '0 2 * * *'      # 每天 02:00 UTC
    # - cron: '0 */12 * * *' # 每 12 小时
    # - cron: '0 2 * * 1'    # 每周一
    # - cron: '0 2 1 * *'    # 每月 1 号
```

### Cron 表达式说明

```
分 时 日 月 周
│ │ │ │ │
│ │ │ │ └─── 星期 (0-6, 0=周日)
│ │ │ └────── 月份 (1-12)
│ │ └─────── 日期 (1-31)
│ └──────── 小时 (0-23)
└───────── 分钟 (0-59)
```

**常用示例**：
- `0 2 * * *` - 每天 02:00
- `0 */6 * * *` - 每 6 小时
- `0 0,12 * * *` - 每天 00:00 和 12:00
- `0 2 * * 1` - 每周一 02:00
- `0 2 1 * *` - 每月 1 号 02:00

### 修改扫描数量

编辑工作流文件中的扫描命令：

```yaml
- name: 🔍 执行扫描
  run: |
    python scan_github.py --auto --max-repos 100  # 修改此处
```

### 添加检测规则

编辑 `config.py` 的 `SENSITIVE_PATTERNS`：

```python
SENSITIVE_PATTERNS = [
    r'sk-[a-zA-Z0-9]{32,}',           # OpenAI
    r'sk-ant-[a-zA-Z0-9_-]{32,}',     # Anthropic
    r'your_custom_pattern',            # 添加自定义规则
]
```

---

## 📖 检测的密钥类型

| 密钥类型 | 格式 | 服务商 |
|---------|------|--------|
| OpenAI API Key | `sk-...` | OpenAI |
| OpenAI Project Key | `sk-proj-...` | OpenAI |
| Anthropic API Key | `sk-ant-...` | Anthropic Claude |
| 环境变量 | `OPENAI_API_KEY=...` | 通用 |
| 环境变量 | `ANTHROPIC_API_KEY=...` | 通用 |

---

## 🛡️ 发现泄露后的处理

### ⚠️ 立即采取的行动

1. **轮换密钥**
   - 登录 API 提供商控制台
   - 删除或禁用泄露的密钥
   - 生成新的密钥

2. **检查使用日志**
   - 查看 API 调用记录
   - 确认是否有异常使用
   - 评估潜在影响

3. **清理 Git 历史**（如果是你的仓库）
   ```bash
   # 使用 BFG Repo-Cleaner
   bfg --replace-text passwords.txt
   
   # 或使用 git-filter-repo
   git filter-repo --invert-paths --path secrets.txt
   ```

4. **更新代码实践**
   - 使用环境变量存储敏感信息
   - 添加 `.gitignore` 规则
   - 配置 pre-commit hooks
   - 启用 GitHub Secret Scanning

### 🛡️ 预防措施

**推荐的做法**：

```python
# ✅ 正确：使用环境变量
import os
api_key = os.getenv('OPENAI_API_KEY')

# ❌ 错误：硬编码密钥
api_key = "sk-proj-xxxxxxxxxxxx"
```

**添加到 `.gitignore`**：

```gitignore
# 环境变量文件
.env
.env.local
.env.*.local

# 配置文件
config.json
secrets.json
credentials.json

# 密钥文件
*.key
*.pem
```

---

## ❓ 常见问题

### Q: 工作流没有自动运行？

**可能原因**：
- GitHub Actions 未启用
- Cron 时间未到（可能延迟 5-15 分钟）
- 仓库是私有的且超出免费额度

**解决方法**：
- 检查 Actions 页面是否有错误
- 手动触发一次测试
- 查看仓库的 Actions 设置

### Q: 提示 "GitHub Token is required"？

**解决方法**：
1. 确认 Secret 名称是 `GH_SCAN_TOKEN`
2. 检查 Token 是否有效且未过期
3. 确认 Token 有正确的权限

### Q: API 速率限制？

**解决方法**：
- 减少 `--max-repos` 参数
- 增加扫描间隔时间
- 确保使用有效的 Token（未认证限制 60 次/小时，认证后 5000 次/小时）

### Q: 如何停止自动扫描？

**方法 1**：禁用工作流
- Actions 页面 → 选择工作流 → "..." → "Disable workflow"

**方法 2**：删除工作流文件
```bash
git rm .github/workflows/scheduled-scan.yml
git commit -m "Disable scheduled scan"
git push
```

### Q: 成本如何？

**GitHub Actions 免费额度**：
- 公开仓库：**完全免费**，无限分钟 ✅
- 私有仓库：每月 2000 分钟（免费计划）

**本项目消耗**：
- 单次扫描（50 仓库）：约 10-20 分钟
- 每天一次：约 300-600 分钟/月

**结论**：公开仓库使用完全免费！

---

## 📁 项目结构

```
ai-scan/
├── .github/workflows/       # GitHub Actions 工作流
│   ├── auto-scan.yml       # 基础自动扫描
│   ├── manual-scan.yml     # 手动扫描
│   └── scheduled-scan.yml  # 增强定时扫描
├── config.py               # 配置（检测规则、关键词）
├── github_scanner.py       # GitHub API 交互
├── secret_detector.py      # 敏感信息检测引擎
├── report_generator.py     # 报告生成器
├── scanner.py              # 主扫描器
├── scan_github.py          # 命令行入口
├── requirements.txt        # Python 依赖
├── .gitignore             # Git 忽略规则
├── LICENSE                # MIT 许可证
└── README.md              # 本文件
```

---

## 🔧 技术栈

- **语言**: Python 3.7+
- **核心库**:
  - `PyGithub` - GitHub API 交互
  - `requests` - HTTP 请求
  - `python-dotenv` - 环境变量管理
- **自动化**: GitHub Actions

---

## 🎯 最佳实践

1. **首次使用**
   - 手动触发小规模测试（5-10 仓库）
   - 检查报告格式和内容
   - 验证 Issue 创建正常

2. **定期审查**
   - 每周查看自动创建的 Issue
   - 及时处理高置信度的发现
   - 定期更新检测规则

3. **合理配置**
   - 日常监控：每天一次
   - 快速迭代期：每 12 小时一次
   - 稳定期：每周一次

4. **保护 Token**
   - 定期轮换 Token（建议 90 天）
   - 使用最小权限原则
   - 不要在日志中打印 Token

---

## 📊 报告示例

```txt
============================================================
       InCloud GitHub 云上扫描器 - 扫描报告
============================================================

扫描类型: auto:ai-projects
扫描开始时间: 2025-01-09 10:30:52
报告生成时间: 2025-01-09 10:35:18
发现的问题总数: 3

============================================================

────────────────────────────────────────────────────────────
🔍 仓库地址: https://github.com/user/repo
   发现问题数: 2
────────────────────────────────────────────────────────────

【问题 #1】
  文件路径: src/config.py
  行号: 15
  发现的 API 密钥: sk-p****************************xyz
  置信度: 🔴 HIGH
  代码片段: OPENAI_API_KEY = "sk-proj-xxxxx..."

【问题 #2】
  文件路径: .env
  行号: 3
  发现的 API 密钥: sk-a****************************abc
  置信度: 🟡 MEDIUM
  代码片段: AI_API_KEY=sk-ant-xxxxx...

============================================================
统计信息
============================================================

🔴 高置信度: 1 个
🟡 中置信度: 2 个
🟢 低置信度: 0 个

总计: 3 个潜在问题
```

---

## ⚠️ 免责声明

- 本工具仅用于**安全研究和合法的安全审计**
- 用户需对使用本工具的行为负责
- 请遵守相关法律法规和 GitHub 使用条款
- 扫描他人仓库前请确保有适当的授权

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

<div align="center">

**使用 GitHub Actions 让你的代码更安全！** 🛡️

Made with ❤️ for Security

</div>