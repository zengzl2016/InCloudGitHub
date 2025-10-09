# 🔍 AI API Key Scanner

<div align="center">

**自动扫描 GitHub 仓库，发现泄露的 AI API 密钥**

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub Actions](https://img.shields.io/badge/automation-GitHub%20Actions-2088FF.svg)](https://github.com/features/actions)

🚀 **完全基于 GitHub Actions，无需本地运行** | 💰 **公开仓库完全免费**

[快速开始](#-快速开始-3-步启动) | [功能特性](#-功能特性) | [工作流说明](#-工作流说明) | [常见问题](#-常见问题)

</div>

---

## 📖 什么是这个工具？

这是一个**自动化的安全扫描工具**，专门用于发现 GitHub 仓库中泄露的 AI API 密钥（如 OpenAI、Anthropic Claude 等）。

### 💡 为什么需要它？

- 🔐 API 密钥泄露可能导致账号被盗用、产生巨额费用
- 🌐 公开仓库中的密钥任何人都可以看到和使用
- ⚠️ 很多开发者不小心将密钥提交到 Git 历史中
- 🔍 手动检查成百上千的仓库非常耗时

### ✨ 这个工具的优势

- ✅ **零配置运行** - Fork 后只需添加一个 Token
- ✅ **全自动化** - 每天自动扫描，无需人工干预
- ✅ **智能检测** - 自动过滤示例代码，减少误报
- ✅ **详细报告** - 生成完整的扫描报告并保存 90 天
- ✅ **即时告警** - 发现问题自动创建 Issue 通知
- ✅ **完全免费** - 基于 GitHub Actions，公开仓库无限使用

---

## 🚀 快速开始 (3 步启动)

### 第 1 步：Fork 本仓库

点击页面右上角的 **`Fork`** 按钮，将仓库 fork 到你的账号下。

<details>
<summary>📸 点击查看截图</summary>

```
在 GitHub 页面右上角：
[Watch ▼] [Fork ▼] [Star]
          ↑↑↑↑
        点击这里
```

Fork 后，你将拥有：`https://github.com/YOUR_USERNAME/ai-scan`

</details>

---

### 第 2 步：配置 GitHub Token

#### 2.1 创建 Personal Access Token

1. **访问 Token 设置页面**
   
   点击这个链接 👉 https://github.com/settings/tokens

2. **生成新 Token**
   
   - 点击 **`Generate new token`** → 选择 **`Generate new token (classic)`**
   
3. **填写信息**
   
   | 字段 | 填写内容 |
   |------|---------|
   | Note | `AI Scanner Token`（备注名称）|
   | Expiration | `90 days` 或更长 |
   | Scopes（权限） | ✅ `public_repo`（必需）<br>✅ `read:org`（可选，用于扫描组织）|

4. **生成并复制**
   
   - 点击页面底部的 **`Generate token`** 按钮
   - ⚠️ **立即复制** Token（格式：`ghp_xxxxxxxxxxxx`）
   - 离开页面后将无法再次查看！

<details>
<summary>🔍 为什么需要这些权限？</summary>

- `public_repo`: 读取公开仓库的代码（扫描必需）
- `read:org`: 读取组织信息（如果要扫描组织仓库）

这些是**最小权限**，不会修改任何代码或仓库。

</details>

---

#### 2.2 添加 Token 到你的仓库

1. **进入你 Fork 的仓库设置**
   
   访问：`https://github.com/YOUR_USERNAME/ai-scan/settings/secrets/actions`
   
   或者：你的仓库页面 → `Settings` → 左侧菜单 `Secrets and variables` → `Actions`

2. **添加新 Secret**
   
   - 点击 **`New repository secret`** 按钮
   - **Name**（名称）: `GH_SCAN_TOKEN`
   - **Value**（值）: 粘贴你刚才复制的 Token
   - 点击 **`Add secret`** 保存

<details>
<summary>⚠️ 重要提示</summary>

- Secret 名称**必须**是 `GH_SCAN_TOKEN`（区分大小写）
- Token 添加后无法查看，只能更新或删除
- Token 是加密存储的，安全可靠

</details>

---

### 第 3 步：启动扫描

配置完成后，你有两种方式启动扫描：

#### 选项 A：手动触发（推荐首次使用）

1. **进入 Actions 页面**
   
   访问：`https://github.com/YOUR_USERNAME/ai-scan/actions`

2. **选择工作流**
   
   在左侧列表中点击：**`AI API Key Scanner - Manual Scan`**

3. **运行工作流**
   
   - 点击右侧的 **`Run workflow`** 下拉按钮
   - 保持默认设置或修改参数：
     - **Scan type**: `auto - 自动搜索AI项目`
     - **Target**: 留空（auto 模式不需要）
     - **Max repos**: `10`（首次建议少量测试）
     - **Create issue**: ✅ 勾选
   - 点击绿色的 **`Run workflow`** 按钮

4. **查看进度**
   
   页面会刷新，显示正在运行的任务，点击进入可查看实时日志。

<details>
<summary>🎯 扫描模式说明</summary>

| 模式 | 说明 | Target 填写 |
|------|------|-----------|
| **auto** | 自动搜索 AI 相关项目 | 留空 |
| **user** | 扫描指定用户的所有仓库 | 用户名，如 `openai` |
| **org** | 扫描指定组织的所有仓库 | 组织名，如 `microsoft` |
| **repo** | 扫描单个仓库 | 仓库全名，如 `user/repo` |

</details>

---

#### 选项 B：自动定时运行

配置完成后，工作流将：
- 🕐 **每天自动运行** - UTC 02:00（北京时间 10:00）
- 📊 **自动生成报告** - 保存在 Artifacts 中
- 🔔 **发现问题自动告警** - 创建 Issue 通知你

你只需等待即可，无需任何操作！

---

## 📊 查看扫描结果

### 1️⃣ 查看运行日志

在 Actions 页面，点击任意运行记录：

```
✅ AI API Key Scanner - Manual Scan #12
   └─ 🔍 执行扫描
      └─ 📊 显示扫描摘要
         └─ ✅ 扫描完成
```

可以看到：
- 扫描了多少个仓库
- 发现了多少个问题
- 每个仓库的扫描状态

---

### 2️⃣ 下载完整报告

1. 滚动到运行详情页面底部
2. 找到 **`Artifacts`** 区域
3. 点击下载报告文件（TXT 格式）

报告包含：
- 📁 仓库地址和文件路径
- 🔑 发现的密钥（部分隐藏保护安全）
- 📊 置信度评级（高/中/低）
- 💡 安全建议

<details>
<summary>📄 报告示例</summary>

```txt
============================================================
       InCloud GitHub 云上扫描器 - 扫描报告
============================================================

扫描类型: auto:ai-projects
发现的问题总数: 3

────────────────────────────────────────────────
🔍 仓库地址: https://github.com/user/repo
   发现问题数: 2
────────────────────────────────────────────────

【问题 #1】
  文件路径: src/config.py
  行号: 15
  发现的 API 密钥: sk-p****************************xyz
  置信度: 🔴 HIGH
  代码片段: OPENAI_API_KEY = "sk-proj-xxxxx..."

────────────────────────────────────────────────
统计信息
────────────────────────────────────────────────

🔴 高置信度: 1 个 ⚠️ 需立即处理
🟡 中置信度: 2 个
🟢 低置信度: 0 个

🛡️ 安全建议:
  1. 立即轮换所有泄露的 API 密钥
  2. 使用环境变量存储敏感信息
  3. 在 .gitignore 中添加敏感文件
```

</details>

---

### 3️⃣ 查看自动创建的 Issue

如果扫描发现问题，会自动创建 Issue：

- 🏷️ 带有 `security` 和 `auto-scan` 标签
- 📋 包含问题摘要和统计信息
- 💡 提供处理建议和步骤
- 🔗 链接到完整报告

前往你的仓库 **Issues** 页签查看。

---

## 🎯 功能特性

### 🔍 智能检测

- ✅ 支持多种 AI API 密钥格式：
  - OpenAI: `sk-...`、`sk-proj-...`
  - Anthropic: `sk-ant-...`
  - 环境变量: `OPENAI_API_KEY=...`、`ANTHROPIC_API_KEY=...`
- ✅ 自动过滤示例代码和占位符
- ✅ 置信度评分（高/中/低）
- ✅ 智能去重

### 📊 详细报告

- ✅ 包含仓库地址、文件路径、行号
- ✅ 显示代码片段和上下文
- ✅ 部分隐藏密钥保护安全
- ✅ 统计分析和安全建议
- ✅ 报告保留 90 天

### 🔔 自动告警

- ✅ 发现问题自动创建 Issue
- ✅ 智能避免重复 Issue
- ✅ 分类标记（security、auto-scan）
- ✅ 包含处理建议

### ⚙️ 灵活配置

- ✅ 4 种扫描模式（auto/user/org/repo）
- ✅ 自定义扫描数量
- ✅ 自定义扫描时间（Cron）
- ✅ 可添加自定义检测规则

---

## 🛠️ 工作流说明

本项目包含 3 个 GitHub Actions 工作流，满足不同需求：

### 1. Manual Scan（手动扫描）⭐ 推荐

**文件**: `.github/workflows/manual-scan.yml`

**触发方式**: 仅手动触发

**适用场景**:
- ✅ 首次测试
- ✅ 按需扫描特定目标
- ✅ 灵活控制参数

**参数说明**:

| 参数 | 说明 | 示例 |
|------|------|------|
| Scan type | 扫描模式 | `auto - 自动搜索AI项目` |
| Target | 扫描目标 | 留空（auto）/ `openai`（user）|
| Max repos | 最大仓库数 | `10` / `50` / `100` |
| Create issue | 是否创建 Issue | ✅ 勾选 |

---

### 2. Auto Scan（自动扫描）

**文件**: `.github/workflows/auto-scan.yml`

**触发方式**: 
- 定时：每天 UTC 02:00
- 手动触发

**适用场景**: 日常自动监控

---

### 3. Scheduled Scan（增强定时扫描）

**文件**: `.github/workflows/scheduled-scan.yml`

**触发方式**: 
- 定时：每天 UTC 02:00
- 手动触发

**适用场景**: 企业级定期安全审计

**特点**:
- 📊 详细的统计分析
- 🧠 智能 Issue 管理
- ⏱️ 超时保护（60 分钟）

---

## ⚙️ 自定义配置

### 修改扫描时间

编辑 `.github/workflows/scheduled-scan.yml` 文件：

```yaml
on:
  schedule:
    - cron: '0 2 * * *'      # 当前：每天 02:00 UTC（北京时间 10:00）
    # - cron: '0 */12 * * *' # 改为：每 12 小时一次
    # - cron: '0 2 * * 1'    # 改为：每周一 02:00
    # - cron: '0 2 1 * *'    # 改为：每月 1 号 02:00
```

**Cron 表达式速查**:

| 表达式 | 说明 | 示例时间 |
|--------|------|----------|
| `0 2 * * *` | 每天一次 | 每天 02:00 |
| `0 */6 * * *` | 每 6 小时 | 00:00, 06:00, 12:00, 18:00 |
| `0 0,12 * * *` | 每天两次 | 00:00 和 12:00 |
| `0 2 * * 1` | 每周一次 | 每周一 02:00 |
| `0 2 1 * *` | 每月一次 | 每月 1 号 02:00 |

<details>
<summary>🕐 时区说明</summary>

- GitHub Actions 使用 **UTC 时区**
- 北京时间 = UTC + 8 小时
- 例如：UTC 02:00 = 北京时间 10:00

</details>

---

### 修改扫描数量

编辑工作流文件中的扫描命令：

```yaml
- name: 🔍 执行扫描
  run: |
    python scan_github.py --auto --max-repos 100  # 修改这个数字
```

**建议值**:
- 测试：5-10
- 日常：50-100
- 深度：100-200

---

### 添加自定义检测规则

编辑 `config.py` 文件：

```python
SENSITIVE_PATTERNS = [
    # 现有规则
    r'sk-[a-zA-Z0-9]{32,}',              # OpenAI
    r'sk-ant-[a-zA-Z0-9_-]{32,}',        # Anthropic
    
    # 添加你的自定义规则
    r'your_custom_api_key_pattern',       # 你的规则
    r'SECRET_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
]
```

---

## ❓ 常见问题

<details>
<summary><b>Q1: 为什么工作流没有自动运行？</b></summary>

**可能原因**:
1. GitHub Actions 未启用
2. Cron 时间未到（首次设置后需等待）
3. 仓库是私有的且超出免费额度

**解决方法**:
1. 检查 Actions 页面是否有错误提示
2. 手动触发一次测试
3. 确认仓库的 Actions 权限已启用

</details>

<details>
<summary><b>Q2: 提示 "GitHub Token is required" 怎么办？</b></summary>

**原因**: Secret 配置不正确

**解决方法**:
1. 确认 Secret 名称是 `GH_SCAN_TOKEN`（注意大小写）
2. 检查 Token 是否过期
3. 验证 Token 有 `public_repo` 权限
4. 重新添加 Secret

</details>

<details>
<summary><b>Q3: 扫描失败，提示 API 速率限制？</b></summary>

**原因**: GitHub API 调用过于频繁

**解决方法**:
1. 减少 `--max-repos` 参数（如改为 20）
2. 增加扫描间隔时间
3. 确保使用了有效的 Token（速率限制更高）
4. 等待 1 小时后重试

</details>

<details>
<summary><b>Q4: 如何停止自动扫描？</b></summary>

**方法 1**: 禁用工作流
- Actions 页面 → 选择工作流 → "..." 菜单 → "Disable workflow"

**方法 2**: 删除或重命名工作流文件
- 删除 `.github/workflows/scheduled-scan.yml`
- 或重命名为 `.github/workflows/scheduled-scan.yml.disabled`

</details>

<details>
<summary><b>Q5: 可以扫描私有仓库吗？</b></summary>

**技术上可以，但需要注意**:

1. Token 需要 `repo` 权限（而不是 `public_repo`）
2. 修改代码中的仓库过滤逻辑
3. 私有仓库扫描需消耗 Actions 分钟数
4. 注意隐私和安全策略

**当前版本**: 设计为只扫描公开仓库，更加安全。

</details>

<details>
<summary><b>Q6: 发现误报怎么办？</b></summary>

**工具特点**:
- 已自动过滤大部分示例代码
- 提供置信度评分
- 建议只关注高置信度的结果

**如果仍有误报**:
1. 检查低置信度的结果，大部分可以忽略
2. 在 `config.py` 中调整检测规则
3. 添加更多过滤条件

</details>

<details>
<summary><b>Q7: 扫描会消耗多少 GitHub Actions 配额？</b></summary>

**GitHub Actions 免费额度**:
- **公开仓库**: 完全免费，无限分钟 ✅
- **私有仓库**: 每月 2000 分钟（免费账户）

**本项目消耗**:
- 单次扫描（50 仓库）: 约 10-20 分钟
- 每天运行一次: 约 300-600 分钟/月

**结论**: 在公开仓库中使用**完全免费**！

</details>

---

## 🛡️ 发现泄露密钥后怎么办？

### ⚠️ 立即采取的 4 个步骤

#### 1️⃣ 立即轮换密钥

- 登录 API 提供商控制台（OpenAI、Anthropic 等）
- **删除或禁用**泄露的密钥
- 生成新的密钥

#### 2️⃣ 检查使用日志

- 查看 API 调用记录
- 确认是否有异常使用
- 评估可能的损失

#### 3️⃣ 清理 Git 历史

如果密钥在你的仓库中：

```bash
# 方法 1: 使用 BFG Repo-Cleaner（推荐）
bfg --replace-text passwords.txt

# 方法 2: 使用 git-filter-repo
git filter-repo --invert-paths --path secrets.txt
```

⚠️ **注意**: 这些操作会改写 Git 历史，需谨慎操作。

#### 4️⃣ 更新代码实践

**正确的做法**:

```python
# ✅ 推荐：使用环境变量
import os
api_key = os.getenv('OPENAI_API_KEY')

# ❌ 错误：硬编码密钥
api_key = "sk-proj-xxxxxxxxxxxx"
```

**更新 `.gitignore`**:

```gitignore
# 环境变量
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
*.p12
```

**配置 pre-commit hooks**:

```bash
# 安装 pre-commit
pip install pre-commit

# 创建配置文件
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
EOF

# 安装 hooks
pre-commit install
```

---

## 📚 相关资源

- 📖 [GitHub Actions 文档](https://docs.github.com/actions)
- 🔐 [GitHub Secret Scanning](https://docs.github.com/code-security/secret-scanning)
- 🛡️ [OpenAI API 安全最佳实践](https://platform.openai.com/docs/guides/safety-best-practices)
- 🔑 [如何保护 API 密钥](https://owasp.org/www-project-api-security/)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 如何贡献

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## ⚠️ 免责声明

- 本工具仅用于**安全研究和合法的安全审计**
- 用户需对使用本工具的行为负责
- 请遵守相关法律法规和 GitHub 使用条款
- 扫描他人仓库前请确保有适当的授权
- 工具可能存在误报或漏报，建议人工复核

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## ⭐ 如果觉得有用

如果这个工具帮助到了你：

- ⭐ 给项目点个 Star
- 🔀 Fork 并使用
- 📢 分享给其他开发者
- 🐛 报告问题或建议改进

---

<div align="center">

### 🛡️ 让你的代码更安全！

**现在就 Fork 并开始使用吧！** 👆

---

Made with ❤️ for Security

</div>