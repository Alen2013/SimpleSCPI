"""
主窗口逻辑类 - 负责 UI 逻辑和业务逻辑的协调
"""
import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5 import QtCore, QtWidgets

from ui.MainUI import Ui_MainWindow
from core.base import BaseObject
from core.instrument import Instrument
from core.exceptions import InstrumentError, ConnectionError, CommunicationError

class TestThread(QThread):
    """测试线程类"""
    msgSignal = pyqtSignal(str)

    def __init__(self, ins, model, cmd_list):
        super().__init__()
        self.msg = ""
        self.runFlag = True
        self.insCtrl = ins
        self.model_cmd = model
        self.cmd = cmd_list
        
    def run(self):
        if not self.insCtrl.is_connected:
            self.msgSignal.emit("Please connect first!") 
            return
        sTime = datetime.now()
        for i in self.cmd:
            if i["Check"]:
                command = i["Command"]
                if command == '':
                    continue
                # 使用 Type 字段判断命令类型
                cmd_type = i["Type"]
                if cmd_type == "query":
                    self.query(command)
                elif cmd_type == "write":
                    self.write(command)
        eTime = datetime.now()
        self.msgSignal.emit(f"Test time {eTime-sTime}") 
             
    def write(self, str):
        sTime = datetime.now()
        self.insCtrl.write(str)
        self.model_cmd.appendRow([
            QStandardItem(f"{sTime.strftime('%H:%M:%S.%f')}"),
            QStandardItem("Write"),
            QStandardItem(''),
            QStandardItem(str)
        ])
    
    def query(self, str):
        sTime = datetime.now()
        ret = self.insCtrl.query(str)
        eTime = datetime.now()
        interval = (eTime-sTime)
        self.model_cmd.appendRow([
            QStandardItem(f"{sTime.strftime('%H:%M:%S.%f')}"),
            QStandardItem("Write"),
            QStandardItem(''),
            QStandardItem(str)
        ])
        self.model_cmd.appendRow([
            QStandardItem(f"{eTime.strftime('%H:%M:%S.%f')}"),
            QStandardItem("Read"),
            QStandardItem(f"{interval}"),
            QStandardItem(ret)
        ])
        return ret

class VLine(QFrame):
    """垂直分割线"""
    def __init__(self):
        super(VLine, self).__init__()
        self.setFrameShape(self.VLine|self.Sunken)

class MainWindow(QMainWindow, Ui_MainWindow, BaseObject):
    """主窗口类"""
    
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        BaseObject.__init__(self)
        
        # 首先设置日志，避免后续调用时 logger 为 None
        self.set_log('MAIN', 'test.log')
        
        self.setupUi(self)
        self.splitter.setSizes([300, 200])
        self.splitter_2.setSizes([400, 180])
        self.StatusSplit()
        self.ToolBarSplit()
        self.checkWidgetList = []
        self.buttonWidgetList = []
        self.typeComboList = []  # 存储类型选择框

        # param
        self.flag = False
        self.testThread = None
        self.setFile = None
        self.savePath = self.execute_path
        print(self.savePath)
        self.model = QStandardItemModel()

        # slots  
        self.actionSave.triggered.connect(self.SaveData)
        self.actionRecall_Setup.triggered.connect(self.LoadSetup)
        
        # instrument
        self.ins = Instrument()
        self.ins.set_log('INS', 'test.log')
        
        # 最后初始化表格（需要在 logger 设置后）
        self.TableWidgetInit()
            
        # tableView
        self.header = ['Time', 'Type', 'Interval(ms)', 'Command']
        self.model_cmd = QStandardItemModel()
        self.model_cmd.setHorizontalHeaderLabels(self.header)
        self.tableView2.setModel(self.model_cmd)
        self.tableView2.horizontalHeader().setStretchLastSection(True)
        # 大小扩展适当尺寸
        self.tableView2.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableView2.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tableView2.setColumnWidth(2, 150)
        self.tableView2.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.tableView2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView2.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView2.customContextMenuRequested.connect(self.ContextMenu)
        self.tableView2.setShowGrid(False)
    
    def ContextMenu(self, pos):
        menu = QMenu()
        item = menu.addAction("Clear")
        screenPos = self.tableView2.mapToGlobal(pos)
        action = menu.exec(screenPos)
        if action == item:
            self.model_cmd.clear()
            self.model_cmd.setHorizontalHeaderLabels(self.header)
            self.tableView2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.tableView2.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self.tableView2.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
            self.tableView2.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
    def TableWidgetInit(self):
        self.cmdList = []  
        
        # 首先尝试加载自动保存的配置（不刷新表格，因为表格还没初始化）
        config_loaded = self.LoadAutoSavedConfig(refresh_table=False)
        
        if not config_loaded:
            # 使用默认命令列表
            self.cmdList.append({"Command": ":SENSe:FREQuency:STARt 500E6", "Comment": "设置起始频率", "Check": False, "Type": "write"})
            self.cmdList.append({"Command": ":SENSe:FREQuency:STOP 6000E6", "Comment": "设置终止频率", "Check": False, "Type": "write"})
            self.cmdList.append({"Command": ":SENSe:SWEep:POINt 201", "Comment": "设置扫描点数", "Check": False, "Type": "write"})
            self.cmdList.append({"Command": ":SENS:ISEGM:BWID 1E3", "Comment": "设置扫描IFBW", "Check": False, "Type": "write"})
            self.cmdList.append({"Command": ":SENS:HOLD:FUNC HOLD", "Comment": "设置扫描方式", "Check": False, "Type": "write"})
            self.cmdList.append({"Command": ":TRIG:SING;*OPC?", "Comment": "单次扫描", "Check": False, "Type": "query"})
            self.Log("使用默认命令配置")
        else:
            self.Log("已加载上次自动保存的配置")
        
        rows = len(self.cmdList)

        # tableWidget
        self.tableWidget_2.setRowCount(rows)
        self.tableWidget_2.setColumnCount(5)  # 增加一列用于显示类型
        self.tableWidget_2.setHorizontalHeaderLabels(["Checked", "Command", "Comment", "Type", "Action"])
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tableWidget_2.setColumnWidth(3, 80)  # Type列宽度，为ComboBox留出足够空间
        self.tableWidget_2.setColumnWidth(4, 150)  # Action列宽度
        self.tableWidget_2.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget_2.customContextMenuRequested.connect(self.SelectMenu)
        
        # 设置行高以确保checkbox和按钮显示完整
        self.tableWidget_2.verticalHeader().setMinimumSectionSize(35)  # 设置最小行高为35像素
        
        for i in range(rows):
            cmd = self.cmdList[i]
            print(cmd)
            
            self.tableWidget_2.setCellWidget(i, 0, self.CreateCheckBox())
            self.tableWidget_2.setItem(i, 1, QTableWidgetItem(cmd["Command"]))
            self.tableWidget_2.setItem(i, 2, QTableWidgetItem(cmd["Comment"]))
            # 创建 Type 列的 ComboBox
            self.tableWidget_2.setCellWidget(i, 3, self.CreateTypeComboBox(cmd["Type"]))
            self.tableWidget_2.setCellWidget(i, 4, self.CreateButton())
        
        # setItem 同样会触发 cellchanged，所以加到最后
        self.tableWidget_2.cellChanged.connect(self.ContextChanged)
        
    def SelectMenu(self, pos):
        colNum = None
        for i in self.tableWidget_2.selectionModel().selection().indexes():
            colNum = i.column()
        
        if colNum is None:
            return
        elif colNum == 0:
            menu = QMenu()
            item1 = menu.addAction("Select All")
            item2 = menu.addAction("Deselect All")
            
            screenPos = self.tableWidget_2.mapToGlobal(pos)
            action = menu.exec(screenPos)
            
            if action == item1:
                self.SelectAll()
            elif action == item2:
                self.DeselectAll()
        else:
            menu = QMenu()
            item3 = menu.addAction("Add Item")
            item4 = menu.addAction("Delete Item")
            
            screenPos = self.tableWidget_2.mapToGlobal(pos)
            action = menu.exec(screenPos)
            
            if action == item3:
                self.AddItem()
            elif action == item4:
                self.DelItem(pos)
            
    def AddItem(self):
        cmd = {"Command": "", "Comment": "", "Check": False, "Type": "write"}
        self.cmdList.append(cmd)
        rows = len(self.cmdList)
        i = rows - 1
        self.tableWidget_2.setRowCount(rows)
        self.tableWidget_2.setCellWidget(i, 0, self.CreateCheckBox())
        self.tableWidget_2.setItem(i, 1, QTableWidgetItem(cmd["Command"]))
        self.tableWidget_2.setItem(i, 2, QTableWidgetItem(cmd["Comment"]))
        # 创建 Type 列的 ComboBox
        self.tableWidget_2.setCellWidget(i, 3, self.CreateTypeComboBox(cmd["Type"]))
        self.tableWidget_2.setCellWidget(i, 4, self.CreateButton())
        
    def DelItem(self, pos):
        row = self.tableWidget_2.indexAt(pos).row()
        print(row)
        self.verticalLayout_2.removeWidget(self.checkWidgetList[row])
        self.verticalLayout_2.removeWidget(self.buttonWidgetList[row])
        self.tableWidget_2.removeRow(row)
        self.cmdList.pop(row)
        self.checkWidgetList[row].deleteLater()
        self.buttonWidgetList[row].deleteLater()
        if row < len(self.typeComboList):
            self.typeComboList[row].deleteLater()
            self.typeComboList.pop(row)
        self.checkWidgetList.pop(row)
        self.buttonWidgetList.pop(row)
    

    def SelectAll(self):
        for widget in self.checkWidgetList:
            btnList = widget.findChildren(QCheckBox)
            for btn in btnList:
                btn.setChecked(True)
        for cmd in self.cmdList:
            cmd["Check"] = True

    def DeselectAll(self):
        for widget in self.checkWidgetList:
            btnList = widget.findChildren(QCheckBox)
            for btn in btnList:
                btn.setChecked(False)
        for cmd in self.cmdList:
            cmd["Check"] = False

    def SelectOne(self):
        pWidget = self.sender()
        row = self.tableWidget_2.indexAt(pWidget.parentWidget().pos()).row()
        print(f"行数：{row}")
        checkBox = self.checkWidgetList[row].findChildren(QCheckBox)
        self.cmdList[row]["Check"] = bool(checkBox[0].isChecked())
    
    def CreateCheckBox(self):
        widget = QtWidgets.QWidget()
        hLayout = QtWidgets.QHBoxLayout()
        cBtn = QtWidgets.QCheckBox()
        
        # 设置布局边距，确保checkbox居中显示
        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.addWidget(cBtn)
        hLayout.setAlignment(cBtn, Qt.AlignCenter)        
        
        widget.setLayout(hLayout)
        self.checkWidgetList.append(widget)
        cBtn.stateChanged.connect(self.SelectOne)
        return widget

    def CreateButton(self):
        widget = QtWidgets.QWidget()
        hLayout = QtWidgets.QHBoxLayout()
        
        # 创建 Send 按钮
        sendBtn = QtWidgets.QPushButton('Send')
        sendBtn.setStyleSheet(''' text-align : center;
                                        height : 30px;
                                        border-style: outset;
                                        font : 13px  ''')
        sendBtn.setToolTip("发送命令 (Write)")
        sendBtn.clicked.connect(self.tableWidgetSend)
        
        # 创建 Query 按钮
        queryBtn = QtWidgets.QPushButton('Query')
        queryBtn.setStyleSheet(''' text-align : center;
                                        height : 30px;
                                        border-style: outset;
                                        font : 13px  ''')
        queryBtn.setToolTip("查询命令 (Query)")
        queryBtn.clicked.connect(self.tableWidgetQuery)
        
        # 添加按钮到布局
        hLayout.addWidget(sendBtn)
        hLayout.addWidget(queryBtn)
        hLayout.setContentsMargins(5, 4, 5, 4)
        widget.setLayout(hLayout)
        
        self.buttonWidgetList.append(widget)
        return widget

    def CreateTypeComboBox(self, cmd_type="write"):
        """创建类型选择下拉框"""
        widget = QtWidgets.QWidget()
        hLayout = QtWidgets.QHBoxLayout()
        comboBox = QtWidgets.QComboBox()
        
        # 添加选项
        comboBox.addItem("write")
        comboBox.addItem("query")
        
        # 设置当前值
        if cmd_type == "query":
            comboBox.setCurrentIndex(1)
        else:
            comboBox.setCurrentIndex(0)
        
        # 连接信号
        comboBox.currentTextChanged.connect(self.TypeComboChanged)
        
        # 设置布局
        hLayout.setContentsMargins(2, 2, 2, 2)
        hLayout.addWidget(comboBox)
        widget.setLayout(hLayout)
        
        self.typeComboList.append(widget)
        return widget

    def TypeComboChanged(self, text):
        """类型选择框变化处理"""
        comboBox = self.sender()
        # 找到对应的行
        for i, widget in enumerate(self.typeComboList):
            if widget.findChildren(QtWidgets.QComboBox)[0] == comboBox:
                if i < len(self.cmdList):
                    self.cmdList[i]["Type"] = text
                    self.Log(f"已更新第{i+1}行命令类型为: {text}")
                break

    def ContextChanged(self, row, col):
        print(col, row)
        context = self.tableWidget_2.item(row, col).text()
        if col == 1:
            self.cmdList[row]["Command"] = context
        elif col == 2:
            self.cmdList[row]["Comment"] = context
        # Type 列 (col == 3) 现在由 ComboBox 处理，不需要在这里处理
        print(self.cmdList)

    def SaveData(self):
        """保存命令配置到文件"""
        import json
        
        # 获取当前命令列表数据
        config_data = {
            "commands": self.cmdList,
            "saved_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "version": "1.0"
        }
        
        # 选择保存文件
        default_name = f"SCPI_Config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        FullFileName, _ = QFileDialog.getSaveFileName(
            self, '保存命令配置', f'./{default_name}',
            'JSON Config File(*.json);;All Files(*.*)'
        )
        
        if FullFileName == "":
            return
            
        try:
            # 保存配置到JSON文件
            with open(FullFileName, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
            
            self.Log(f"配置已保存到: {FullFileName}")
            self.Log(f"共保存 {len(self.cmdList)} 条命令")
            
        except Exception as e:
            self.Log(f"保存配置失败: {str(e)}")
            QMessageBox.warning(self, "保存失败", f"无法保存配置文件:\n{str(e)}")
               
    def LoadSetup(self):
        """加载命令配置文件"""
        import json
        
        fullFileName = QFileDialog.getOpenFileName(
            self, '加载命令配置', '.\\', "JSON Config File(*.json);;All Files(*.*)"
        )
        
        if fullFileName[0] == "":
            return
            
        try:
            # 加载配置文件
            with open(fullFileName[0], 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # 验证配置文件格式
            if "commands" not in config_data:
                QMessageBox.warning(self, "加载失败", "配置文件格式不正确")
                return
                
            # 更新命令列表
            self.cmdList = config_data["commands"]
            
            # 重新初始化表格
            self.RefreshTableWidget()
            
            # 记录日志
            saved_time = config_data.get("saved_time", "未知时间")
            self.Log(f"配置已加载: {fullFileName[0]}")
            self.Log(f"保存时间: {saved_time}")
            self.Log(f"共加载 {len(self.cmdList)} 条命令")
            
        except json.JSONDecodeError:
            QMessageBox.warning(self, "加载失败", "配置文件格式错误，无法解析JSON")
            self.Log("配置文件JSON格式错误")
        except Exception as e:
            QMessageBox.warning(self, "加载失败", f"无法加载配置文件:\n{str(e)}")
            self.Log(f"加载配置失败: {str(e)}")
    
    def RefreshTableWidget(self):
        """刷新表格显示"""
        # 清空现有的widget列表
        for widget in self.checkWidgetList + self.buttonWidgetList + self.typeComboList:
            widget.deleteLater()
        self.checkWidgetList.clear()
        self.buttonWidgetList.clear()
        self.typeComboList.clear()
        
        # 重新设置表格
        rows = len(self.cmdList)
        self.tableWidget_2.setRowCount(rows)
        
        # 设置行高以确保checkbox和按钮显示完整
        self.tableWidget_2.verticalHeader().setMinimumSectionSize(35)  # 设置最小行高为35像素
        
        # 安全地断开信号连接，避免在设置过程中触发
        try:
            self.tableWidget_2.cellChanged.disconnect()
        except TypeError:
            # 如果没有连接的信号，会抛出 TypeError，这是正常的
            pass
        
        for i in range(rows):
            cmd = self.cmdList[i]
            
            # 创建复选框
            checkbox_widget = self.CreateCheckBox()
            self.tableWidget_2.setCellWidget(i, 0, checkbox_widget)
            
            # 设置复选框状态
            checkbox = checkbox_widget.findChildren(QCheckBox)[0]
            checkbox.setChecked(cmd.get("Check", False))
            
            # 设置命令和注释
            self.tableWidget_2.setItem(i, 1, QTableWidgetItem(cmd.get("Command", "")))
            self.tableWidget_2.setItem(i, 2, QTableWidgetItem(cmd.get("Comment", "")))
            # 创建 Type 列的 ComboBox
            cmd_type = cmd.get("Type", "write")
            self.tableWidget_2.setCellWidget(i, 3, self.CreateTypeComboBox(cmd_type))
            
            # 创建按钮
            self.tableWidget_2.setCellWidget(i, 4, self.CreateButton())
        
        # 重新连接信号
        self.tableWidget_2.cellChanged.connect(self.ContextChanged)  

    def StartTest(self):
        if self.testThread is None or self.testThread.isFinished():
            self.testThread = TestThread(self.ins, self.model_cmd, self.cmdList)
            self.testThread.msgSignal.connect(self.Log)
            self.testThread.start()
 
    def StatusSplit(self):
        self.lbl2 = QLabel("Status : ")
        self.statusBar().reformat()
        self.statusBar().addPermanentWidget(VLine())
        self.statusBar().addPermanentWidget(self.lbl2)
        self.lbl2.setText("Status : UnConnected")
         
    def ToolBarSplit(self):
        self.label_timeout = QLabel(" Timeout(ms):")
        self.label_timeout.setStyleSheet('''background-color:#455364''')
        self.lineEdit_timeOut = QLineEdit("5000")
        self.lineEdit_timeOut.setMaximumSize(QtCore.QSize(70, 27))
        self.toolBar.addWidget(self.label_timeout)
        self.toolBar.addWidget(self.lineEdit_timeOut)
        
        self.label_terminate = QLabel('Termination:')
        self.label_terminate.setStyleSheet('''background-color:#455364''')
        self.comboBox_Termination = QComboBox()
        self.comboBox_Termination.setMaximumSize(QtCore.QSize(310, 27))
        self.comboBox_Termination.insertItem(0, '\\n')
        self.comboBox_Termination.insertItem(1, "\\r")
        self.comboBox_Termination.insertItem(2, '')
        self.toolBar.addWidget(self.label_terminate)
        self.toolBar.addWidget(self.comboBox_Termination)

        self.label_addr = QLabel(" Address:")
        self.label_addr.setStyleSheet('''background-color:#455364''')
        self.lineEdit_addr = QLineEdit("TCPIP0::127.0.0.1::5001::SOCKET")
        self.lineEdit_addr.setMaximumSize(QtCore.QSize(310, 27))
        self.toolBar.addWidget(self.label_addr)
        self.toolBar.addWidget(self.lineEdit_addr)

        self.tBtn_connect = QAction("Connect", self)
        self.toolBar.addAction(self.tBtn_connect)
        # self.toolBar.addSeparator() 

        # self.label_hex = QLabel(" Hex:")
        # self.label_hex.setStyleSheet('''background-color:#455364''')
        # self.checkBox_hex = QCheckBox()
        # self.checkBox_hex.setMaximumSize(QtCore.QSize(70, 27))
        # self.toolBar.addWidget(self.label_hex)
        # self.toolBar.addWidget(self.checkBox_hex)

        self.toolBar.addSeparator() 
        self.tBtn_run = QAction(QIcon(":/run.png"), "运行", self)
        self.toolBar.addAction(self.tBtn_run)
        
        widget_spacer = QWidget() 
        widget_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum) 
        self.tBtn_connect.triggered.connect(self.Connect)
        self.tBtn_run.triggered.connect(self.StartTest)
      
    def Connect(self):
        conStr = self.lineEdit_addr.text().strip()
        timeout = int(self.lineEdit_timeOut.text().strip())
        terminate = self.comboBox_Termination.currentText()
        if terminate == "\\n":
            terminate = '\n'
        elif terminate == '\\r':
            terminate = '\r'
        self.logger.info(conStr)

        if self.tBtn_connect.text() == "Connect":
            try:
                # 记录连接开始时间
                connect_time = datetime.now()
                
                self.ins.open(conStr, timeout, termination=terminate)
                self.insType = self.ins.instrument_id
                self.lbl2.setText("Status : Connected")
                self.tBtn_connect.setText("Disconnect")
                self.Log("Connected to " + conStr + " successfully") 
                # 将 *IDN? 命令和响应添加到 I/O 表格中
                # 因为 ins.open() 内部已经执行了 *IDN? 查询，我们需要在界面上显示这个过程
                idn_cmd = "*IDN?"
                idn_response = self.ins.instrument_id
                
                # 添加 Write 记录
                self.model_cmd.appendRow([
                    QStandardItem(f"{connect_time.strftime('%H:%M:%S.%f')}"),
                    QStandardItem("Write"),
                    QStandardItem(''),
                    QStandardItem(idn_cmd)
                ])
                
                # 添加 Read 记录
                read_time = datetime.now()
                interval = read_time - connect_time
                self.model_cmd.appendRow([
                    QStandardItem(f"{read_time.strftime('%H:%M:%S.%f')}"),
                    QStandardItem("Read"),
                    QStandardItem(f"{interval}"),
                    QStandardItem(idn_response)
                ])
                
                # 滚动到底部显示最新记录
                self.tableView2.scrollToBottom()
                
            except (ConnectionError, CommunicationError) as e:
                self.logger.error(f"Connect error: {e}")
                self.statusBar().showMessage("Connect error!")  
        else:
            self.ins.close()
            self.tBtn_connect.setText("Connect")
            self.lbl2.setText("Status : Disconnect") 
         
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, '提示', "确定要退出吗?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
            self.AutoSaveConfig()  # 自动保存配置
            if self.ins.is_connected:
                self.ins.close() 
        else:
            event.ignore()
    
    def AutoSaveConfig(self):
        """自动保存配置到默认文件"""
        import json
        
        try:
            config_data = {
                "commands": self.cmdList,
                "saved_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "version": "1.0",
                "auto_saved": True
            }
            
            # 保存到默认配置文件
            config_file = "scpi_config_auto.json"
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
            
            self.Log(f"配置已自动保存到: {config_file}")
            
        except Exception as e:
            self.Log(f"自动保存配置失败: {str(e)}")
    
    def LoadAutoSavedConfig(self, refresh_table=True):
        """加载自动保存的配置"""
        import json
        
        config_file = "scpi_config_auto.json"
        if not os.path.exists(config_file):
            return False
            
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            if "commands" in config_data and config_data.get("auto_saved", True):
                self.cmdList = config_data["commands"]
                if refresh_table:
                    self.RefreshTableWidget()
                return True
                
        except Exception as e:
            self.Log(f"加载自动保存配置失败: {str(e)}")
            
        return False

    def Log(self, str):
        self.logger.info(f"{str}")
        timeTmp = f"{datetime.now().strftime('%H:%M:%S.%f')}"[:-3]  
        self.textBrowser.append(f"{timeTmp} {str}")
        self.tableView2.scrollToBottom()

    def tableWidgetSend(self, str):
        pWidget = self.sender()
        row = self.tableWidget_2.indexAt(pWidget.parentWidget().pos()).row()
        cmd = self.cmdList[row]['Command']
        self.SendCmd(cmd)

    def tableWidgetQuery(self, str):
        pWidget = self.sender()
        row = self.tableWidget_2.indexAt(pWidget.parentWidget().pos()).row()
        cmd = self.cmdList[row]['Command']
        self.QueryCmd(cmd)

    def SendCmd(self, cmd): 
        if not self.ins.is_connected:
            self.Log("Please connect first!") 
            return

        sTime = datetime.now()
        try:
            # if self.checkBox_hex.checkState():
            #     cmd = bytes.fromhex(cmd)
            #     print(cmd)              

            self.ins.write(cmd)
            self.model_cmd.appendRow([
                QStandardItem(f"{sTime.strftime('%H:%M:%S.%f')}"),
                QStandardItem("Write"),
                QStandardItem(''),
                QStandardItem(str(cmd))
            ])
        except (CommunicationError, InstrumentError) as e:
            self.Log(f"Write failed: {e}")
            
        self.tableView2.scrollToBottom()

    def QueryCmd(self, cmd):
        if not self.ins.is_connected:
            self.Log("Please connect first!") 
            return

        sTime = datetime.now()
        try:
            ret = self.ins.query(cmd)
            eTime = datetime.now()
            interval = eTime - sTime
            self.model_cmd.appendRow([
                QStandardItem(f"{sTime.strftime('%H:%M:%S.%f')}"),
                QStandardItem("Write"),
                QStandardItem(''),
                QStandardItem(cmd)
            ])
            self.model_cmd.appendRow([
                QStandardItem(f"{eTime.strftime('%H:%M:%S.%f')}"),
                QStandardItem("Read"),
                QStandardItem(f"{interval}"),
                QStandardItem(ret)
            ])
        except (CommunicationError, InstrumentError) as e:
            self.Log(f"Query failed: {e}")
            
        self.tableView2.scrollToBottom()

    def NoRound(self, numeric, num):
        num_x, num_y = str(numeric).split('.')
        num = f'{num_x}.{num_y[:num]}'   
        return num 