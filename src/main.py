#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SimpleSCPI - 简单 SCPI 仪器控制软件
主程序入口
"""
import sys
import os
import time
import ctypes

# 修复 PyInstaller 打包后的模块导入问题
def fix_import_path():
    """修复模块导入路径"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后的临时目录
        base_path = sys._MEIPASS
        # 添加所有需要的路径
        paths_to_add = [
            base_path,
            os.path.join(base_path, 'ui'),
            os.path.join(base_path, 'core'),
            os.path.join(base_path, 'resources')
        ]
    else:
        # 开发环境
        current_dir = os.path.dirname(os.path.abspath(__file__))
        paths_to_add = [
            current_dir,
            os.path.join(current_dir, 'ui'),
            os.path.join(current_dir, 'core'),
            os.path.join(current_dir, 'resources')
        ]
    
    # 将路径添加到 sys.path 的开头
    for path in reversed(paths_to_add):
        if path not in sys.path:
            sys.path.insert(0, path)

# 在导入其他模块之前修复路径
fix_import_path()

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QSplashScreen
import qdarkstyle

# 现在尝试导入项目模块
try:
    from ui.main_window import MainWindow
    from resources import ico_rc
except ImportError as e:
    print(f"Import error: {e}")
    # 尝试直接导入
    try:
        import main_window as MainWindow_module
        MainWindow = MainWindow_module.MainWindow
        import ico_rc
    except ImportError as e2:
        print(f"Second import error: {e2}")
        sys.exit(1)

# 设置应用程序ID（Windows）
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("SimpleSCPI")
except AttributeError:
    pass  # 非 Windows 系统

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    
    # 显示启动画面
    #splash = QSplashScreen(QPixmap(':/Logo.png'))
    #splash.show()
    #time.sleep(1)
    app.processEvents()  # 防止进程卡死
    
    # 创建主窗口
    main_window = MainWindow()
    main_window.show()
    
    # 隐藏启动画面
    #splash.finish(main_window)
    
    # 启动应用程序
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()