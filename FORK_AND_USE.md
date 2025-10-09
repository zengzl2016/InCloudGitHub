# 🔀 Fork 后使用指南

本文档专门为 **Fork 本仓库** 的用户提供详细的配置和使用说明。

---

## ✅ 前提条件

- ✅ 拥有 GitHub 账号
- ✅ 已 Fork 本仓库到你的账号下

---

## 📋 配置步骤

### Step 1: 确认 Fork 成功

访问你的 GitHub 主页，应该能看到：

```
https://github.com/YOUR_USERNAME/ai-scan
```

如果看到 `forked from ORIGINAL_REPO`，说明 Fork 成功。

---

### Step 2: 启用 GitHub Actions

1. 访问你 Fork 的仓库
2. 点击 **`Actions`** 标签
3. 如果看到 "Workflows aren't being run on this forked repository"
4. 点击 **`I understand my workflows, go ahead and enable them`**

---

### Step 3: 创建 GitHub Token

#### 3.1 访问 Token 设置

直接访问：https://github.com/settings/tokens

或者：
1. 点击右上角头像
2. Settings → Developer settings → Personal access tokens → Tokens (classic)

#### 3.2 生成新 Token

1. 点击 **`Generate new token`** → **`Generate new token (classic)`**
2. 填写表单：

| 字段 | 值 |
|------|-----|
| **Note** | `AI Scanner Token`（或任意描述）|
| **Expiration** | `90 days`（或 `No expiration`）|
| **Scopes** | |
| └─ repo | ❌ 不勾选 |
| └─ **public_repo** | ✅ **勾选（必需）** |
| └─ admin:org | ❌ 不勾选 |
| └─ **read:org** | ✅ **勾选（可选，用于扫描组织）** |

3. 滚动到底部，点击 **`Generate token`**
4. **立即复制** Token（格式类似：`ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx`）

⚠️ **重要**：离开页面后无法再次查看 Token！

---

### Step 4: 添加 Token 到仓库 Secret

#### 4.1 访问 Secrets 设置

访问：`https://github.com/YOUR_USERNAME/ai-scan/settings/secrets/actions`

或者：
1. 你的仓库页面
2. **Settings** 标签
3. 左侧菜单：**Secrets and variables** → **Actions**

#### 4.2 添加 Secret

1. 点击 **`New repository secret`** 按钮
2. 填写信息：
   - **Name**: `GH_SCAN_TOKEN` （⚠️ 必须完全一致，区分大小写）
   - **Value**: 粘贴刚才复制的 Token
3. 点击 **`Add secret`** 保存

#### 4.3 验证

Secret 添加成功后，你会在列表中看到：

```
GH_SCAN_TOKEN
Updated now
```

---

## 🚀 运行扫描

### 方式 1: 手动触发（推荐首次）

#### Step 1: 进入 Actions 页面

访问：`https://github.com/YOUR_USERNAME/ai-scan/actions`

#### Step 2: 选择工作流

在左侧列表中点击：
```
AI API Key Scanner - Manual Scan
```

#### Step 3: 运行工作流

1. 点击右侧的 **`Run workflow`** 下拉按钮
2. 填写参数：

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| **Scan type** | `auto - 自动搜索AI项目` | 扫描模式 |
| **Target** | 留空 | auto 模式不需要 |
| **Max repos** | `10` | 首次建议少量 |
| **Create issue** | ✅ 勾选 | 发现问题时创建 Issue |

3. 点击绿色的 **`Run workflow`** 按钮

#### Step 4: 查看运行状态

- 页面会自动刷新，显示运行任务
- 点击任务可查看详细日志
- 等待完成（通常 5-15 分钟）

---

### 方式 2: 自动定时运行

配置完成后，工作流会自动运行：

- ⏰ **运行时间**：每天 UTC 02:00（北京时间 10:00）
- 📊 **自动生成报告**：保存在 Artifacts
- 🔔 **自动告警**：发现问题时创建 Issue

无需任何操作，完全自动化！

---

## 📊 查看结果

### 1. 实时日志

**位置**：Actions 页面 → 点击运行记录

可以看到：
- ✅ 每个步骤的执行状态
- 📋 扫描进度和发现的问题
- ⚠️ 错误信息（如果有）

---

### 2. 下载报告

**位置**：运行详情页 → 底部 Artifacts 区域

报告内容：
- 📁 仓库地址和文件路径
- 🔑 发现的密钥（部分隐藏）
- 📊 置信度评级
- 💡 安全建议

报告保留 **90 天**。

---

### 3. 查看 Issue

**位置**：你的仓库 → Issues 标签

如果发现问题：
- 🏷️ 自动创建 Issue，带 `security` 标签
- 📋 包含问题摘要和统计
- 💡 提供处理建议

---

## ⚙️ 自定义配置

### 修改扫描时间

编辑 `.github/workflows/scheduled-scan.yml`：

```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # 改为你想要的时间
```

**常用时间**：
- `0 2 * * *` - 每天 02:00 UTC
- `0 */12 * * *` - 每 12 小时
- `0 2 * * 1` - 每周一
- `0 2 1 * *` - 每月 1 号

### 修改扫描数量

编辑工作流中的命令：

```yaml
python scan_github.py --auto --max-repos 50  # 改为你需要的数量
```

---

## 🔄 保持同步

### 同步上游更新

如果原仓库有更新，你可以同步：

#### 方法 1: GitHub Web 界面

1. 访问你的 Fork 仓库
2. 如果有更新，会显示 "This branch is X commits behind..."
3. 点击 **`Sync fork`** → **`Update branch`**

#### 方法 2: Git 命令行

```bash
# 添加上游仓库
git remote add upstream https://github.com/ORIGINAL_OWNER/ai-scan.git

# 获取上游更新
git fetch upstream

# 合并更新
git checkout main
git merge upstream/main

# 推送到你的 Fork
git push origin main
```

---

## ❓ 常见问题

### Q: Secret 填错了怎么办？

A: 可以更新或删除
1. Settings → Secrets and variables → Actions
2. 点击 Secret 名称
3. 选择 **Update** 或 **Remove**

### Q: 工作流没有运行？

A: 检查以下几点
- ✅ Actions 已启用
- ✅ Secret 名称是 `GH_SCAN_TOKEN`
- ✅ Token 未过期
- ✅ Token 有正确权限

### Q: 如何停止自动扫描？

A: 禁用工作流
1. Actions 页面
2. 选择工作流
3. 右上角 "..." → "Disable workflow"

---

## 📞 获取帮助

- 📖 查看 [README.md](README.md)
- 🐛 提交 [Issue](../../issues)
- 💬 查看 [FAQ](README.md#-常见问题)

---

<div align="center">

**🎉 配置完成！享受自动化安全扫描吧！**

</div>
