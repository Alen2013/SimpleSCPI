# 快速开始

## 1. 安装环境

### 使用 Conda（推荐）
```bash
# 创建环境
conda env create -f environment.yml
conda activate simplescpi
```

### 使用 pip
```bash
# 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 安装依赖
pip install -r requirements.txt
```

## 2. 运行程序

```bash
cd src
python main.py
```

## 3. 基本使用

1. **连接仪器**：在工具栏输入仪器地址，点击 Connect
2. **添加命令**：右键命令列表 → Add Item
3. **执行命令**：点击 Send 或 Query 按钮
4. **查看结果**：在右侧 I/O 面板查看响应

## 4. 常见地址格式

- TCP/IP: `TCPIP0::192.168.1.100::5001::SOCKET`
- USB: `USB0::0x1234::0x5678::SN123456::INSTR`
- 串口: `ASRL1::INSTR`

## 5. 打包程序（可选）

如果需要创建独立的可执行文件：

```bash
# 安装 PyInstaller
pip install pyinstaller

# 打包程序
pyinstaller SimpleSCPI.spec
```

打包后的程序位于 `dist/SimpleSCPI.exe`。

## 6. 需要帮助？

查看 [README.md](README.md) 了解详细使用说明。 