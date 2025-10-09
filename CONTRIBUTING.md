# 贡献指南

感谢你对本项目的关注！我们欢迎所有形式的贡献。

## 🎯 贡献方式

### 1. 报告问题

发现 Bug 或有新想法？

1. 前往 [Issues](../../issues) 页面
2. 点击 "New issue"
3. 详细描述问题或建议：
   - 问题描述
   - 重现步骤
   - 预期行为
   - 实际行为
   - 环境信息（如有）

### 2. 提交代码

想要贡献代码？

1. **Fork 本仓库**
   ```bash
   # 点击页面右上角的 Fork 按钮
   ```

2. **克隆到本地**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-scan.git
   cd ai-scan
   ```

3. **创建功能分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/bug-description
   ```

4. **进行修改**
   - 遵循现有代码风格
   - 添加必要的注释
   - 更新相关文档

5. **提交更改**
   ```bash
   git add .
   git commit -m "feat: add some feature"
   ```

   提交信息格式：
   - `feat:` - 新功能
   - `fix:` - Bug 修复
   - `docs:` - 文档更新
   - `style:` - 代码格式（不影响功能）
   - `refactor:` - 重构
   - `test:` - 测试相关
   - `chore:` - 构建/工具链更新

6. **推送到 GitHub**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **创建 Pull Request**
   - 访问你的 Fork 仓库
   - 点击 "Compare & pull request"
   - 填写 PR 描述
   - 等待审核

## 📝 代码规范

### Python 代码

- 遵循 PEP 8 规范
- 使用 4 空格缩进
- 函数和类添加 docstring
- 变量命名要有意义

示例：
```python
def scan_repository(repo_name: str) -> List[Dict]:
    """
    扫描指定的 GitHub 仓库
    
    Args:
        repo_name: 仓库全名（如 owner/repo）
    
    Returns:
        检测到的问题列表
    """
    # 实现代码
    pass
```

### YAML 配置

- 使用 2 空格缩进
- 添加必要的注释
- 保持结构清晰

## 🧪 测试

在提交 PR 前，请确保：

1. **代码可以运行**
   ```bash
   python scan_github.py --help
   ```

2. **Python 语法检查**
   ```bash
   python -m py_compile *.py
   ```

3. **工作流配置有效**
   - 检查 YAML 语法
   - 确保工作流可以正常触发

## 💡 建议的贡献方向

### 功能增强

- [ ] 支持更多 AI 服务商的密钥格式
- [ ] 添加更多检测规则
- [ ] 支持 JSON/HTML 报告格式
- [ ] 添加邮件/Slack 通知
- [ ] 支持自定义过滤规则

### 文档改进

- [ ] 添加更多使用示例
- [ ] 翻译成其他语言
- [ ] 添加视频教程
- [ ] 完善 FAQ

### Bug 修复

- [ ] 修复已知问题
- [ ] 提高稳定性
- [ ] 优化性能

## 📋 行为准则

- 尊重所有贡献者
- 建设性的讨论
- 接受不同观点
- 专注于对项目最有利的事情

## 📞 联系方式

- 提交 Issue：[GitHub Issues](../../issues)
- 讨论区：[GitHub Discussions](../../discussions)（如果启用）

---

感谢你的贡献！🎉
