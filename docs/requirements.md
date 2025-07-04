# SimpleSCPI 项目需求文档

## 1. 项目背景
仪器仪表研发、测试等场景中，工程师常需通过SCPI协议对设备进行程控调试。现有如NI MAX等工具虽功能强大，但操作繁琐、不够轻量。SimpleSCPI旨在提供一款更便捷、美观、易用的SCPI指令调试工具，提升调试效率和体验。

## 2. 项目目标
- 支持基于NI VISA的多协议（TCP/IP、GPIB、USB等）SCPI通讯。
- 提供Write、Query、Read、ReadByte等基本SCPI命令操作。
- 支持单条/批量指令发送，便于功能验证和自动化测试。
- 提供美观、现代化的WPF界面，操作便捷。
- 通讯模块独立，便于在其他项目中复用。

## 3. 功能需求
### 3.1 通讯管理
- 支持VISA协议地址输入与连接/断开
- 支持超时、终止符等参数设置
- 通讯相关功能封装为独立类库，UI与通讯解耦

### 3.2 SCPI指令操作
- 支持Write、Query、Read、ReadByte等基本命令
- 支持单条指令和批量指令发送
- 指令可编辑、注释、分组、勾选

### 3.3 界面交互
- 参考原型图布局，操作便捷
- 指令列表支持单独Write/Query按钮
- Trace区实时显示通讯日志
- 结果区显示Query返回、错误、耗时等
- 状态栏显示连接状态、错误提示

### 3.4 美观易用
- 现代化UI风格，支持主题切换
- 支持日志导出、清空

## 4. 非功能需求
- 稳定性高，异常处理完善
- 易于扩展和维护
- 支持后续功能扩展（如脚本、自动化等）
- 通讯模块可独立测试和复用

## 5. 技术选型
- .NET 8.0
- WPF
- CommunityToolkit.Mvvm
- NI VISA（NationalInstruments.VisaNS 或 Ivi.Visa.Interop）
- 可选WPF美化库（如MaterialDesignInXamlToolkit、HandyControl等）
- **通讯模块（SimpleSCPI.Comm）独立为类库，便于多项目复用**

## 6. 目录结构建议

```
SimpleSCPI/
│
├─ SimpleSCPI.sln                // 解决方案文件
├─ README.md                     // 项目说明
├─ docs/                         // 需求、设计等文档
│   └─ requirements.md
│
├─ src/                          // 主程序源码
│   ├─ SimpleSCPI.UI/            // WPF主项目（仅UI和ViewModel）
│   ├─ SimpleSCPI.Comm/          // 通讯类库（VISA/SCPI相关，供UI及其他项目复用）
│   ├─ Models/                   // 通用数据模型（如需多项目共用可移至类库）
│   ├─ ViewModels/               // 视图模型（如仅UI用可保留在UI项目）
│   ├─ Views/                    // 视图
│   ├─ Services/                 // 仅UI相关服务（如业务逻辑、Trace等）
│   ├─ Resources/
│   └─ Utils/
│
└─ SimpleSCPI.Tests/             // 单元测试项目（可为Comm和UI分别建测试）
```

- **SimpleSCPI.Comm/**：封装VISA通讯、SCPI命令、设备发现、异常处理等，暴露接口供UI或其他项目调用。
- **SimpleSCPI.UI/**：只负责界面、用户交互、MVVM绑定，通讯通过依赖注入或接口调用Comm模块。

---

如需详细设计文档或功能分解，可在此基础上进一步细化。 