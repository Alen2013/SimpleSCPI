#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SimpleSCPI - 简单 SCPI 仪器控制软件
主程序入口
"""
import sys
import time
import ctypes
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QSplashScreen
import qdarkstyle

from ui.main_window import MainWindow
from resources import ico_rc

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