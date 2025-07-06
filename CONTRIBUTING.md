# 贡献指南

感谢您对 SimpleSCPI 的关注！我们欢迎各种形式的贡献。

## 🐛 报告问题

1. 查看 [现有 Issues](../../issues) 确认问题未被报告
2. 创建新的 Issue，包含以下信息：
   - 操作系统和 Python 版本
   - 详细的错误信息
   - 复现步骤
   - 预期行为和实际行为

## 🔧 代码贡献

### 开发环境设置

```bash
# Fork 并克隆项目
git clone https://github.com/Alen2013/SimpleSCPI.git
cd SimpleSCPI

# 创建虚拟环境
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 开发流程

1. 创建分支：`git checkout -b feature/your-feature`
2. 编写代码并测试
3. 提交代码：`git commit -m "描述你的更改"`
4. 推送分支：`git push origin feature/your-feature`
5. 创建 Pull Request

### 代码规范

- 遵循 PEP 8 编码规范
- 添加必要的注释和文档字符串
- 确保代码能正常运行

## 📝 提交信息格式

```
类型: 简短描述

详细描述（可选）
```

类型：
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构

## 📞 获得帮助

如果有任何问题，请：
1. 查看现有的 [Issues](../../issues)
2. 创建新的 Issue 进行讨论

感谢您的贡献！🎉 