"""
仪器控制类 - 负责与 SCPI 仪器的通信
"""
import pyvisa as visa
from datetime import datetime
from core.base import BaseObject
from core.exceptions import ConnectionError, CommunicationError

class Instrument(BaseObject):
    """仪器控制类"""
    
    def __init__(self, visa_dll_path='c:/windows/system32/visa32.dll'):
        super().__init__()
        try:
            self.resource_manager = visa.ResourceManager(visa_dll_path)
        except Exception as e:
            raise ConnectionError(f"Failed to initialize VISA resource manager: {e}")
        
        self.instrument_ctrl = None
        self.instrument_id = None
        self.is_connected = False
        
    def open(self, resource_name, timeout=5000, termination=''):
        """
        打开仪器连接
        
        Args:
            resource_name (str): 仪器资源名称
            timeout (int): 超时时间（毫秒）
            termination (str): 终止符
            
        Returns:
            bool: 连接是否成功
            
        Raises:
            ConnectionError: 连接失败时抛出
        """
        try:
            self.instrument_ctrl = self.resource_manager.open_resource(
                resource_name, 
                read_termination=termination
            )
            self.is_connected = True
            self.instrument_ctrl.timeout = timeout
            self.instrument_ctrl.clear()
            self.instrument_id = self.query("*IDN?")
            
            if self.logger:
                self.logger.info(f"Successfully connected to {resource_name}")
                self.logger.info(f"Instrument ID: {self.instrument_id}")
                
            return True
            
        except Exception as e:
            error_msg = f"Failed to connect to {resource_name}: {e}"
            if self.logger:
                self.logger.error(error_msg)
            raise ConnectionError(error_msg)

    def write(self, command):
        """
        向仪器写入命令
        
        Args:
            command (str): SCPI 命令
            
        Raises:
            CommunicationError: 通信失败时抛出
        """
        if not self.is_connected or not self.instrument_ctrl:
            raise CommunicationError("Instrument not connected")
            
        try:
            if self.logger:
                self.logger.info(f"Write: {command}")
            self.instrument_ctrl.write(command)
            
        except Exception as e:
            error_msg = f"Write command failed: {e}"
            if self.logger:
                self.logger.error(error_msg)
            raise CommunicationError(error_msg)

    def query(self, command):
        """
        向仪器发送查询命令并返回结果
        
        Args:
            command (str): SCPI 查询命令
            
        Returns:
            str: 仪器返回的结果
            
        Raises:
            CommunicationError: 通信失败时抛出
        """
        if not self.is_connected or not self.instrument_ctrl:
            raise CommunicationError("Instrument not connected")
            
        try:
            if self.logger:
                self.logger.info(f"Query: {command}")
            self.instrument_ctrl.clear()
            result = self.instrument_ctrl.query(command).strip()
            if self.logger:
                self.logger.info(f"Response: {result}")
            return result
            
        except Exception as e:
            error_msg = f"Query command failed: {e}"
            if self.logger:
                self.logger.error(error_msg)
            raise CommunicationError(error_msg)

    def clear_buffer(self):
        """
        清除仪器接收缓冲区
        
        Raises:
            CommunicationError: 通信失败时抛出
        """
        if not self.is_connected or not self.instrument_ctrl:
            raise CommunicationError("Instrument not connected")
            
        try:
            self.instrument_ctrl.clear()
            if self.logger:
                self.logger.info("Instrument buffer cleared")
                
        except Exception as e:
            error_msg = f"Clear buffer failed: {e}"
            if self.logger:
                self.logger.error(error_msg)
            raise CommunicationError(error_msg)

    def close(self):
        """关闭仪器连接"""
        try:
            if self.instrument_ctrl:
                self.instrument_ctrl.close()
                self.instrument_ctrl = None
                self.is_connected = False
                
                if self.logger:
                    self.logger.info("Instrument connection closed")
                    
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Error closing instrument: {e}")

    def __del__(self):
        """析构函数，确保连接被正确关闭"""
        self.close()

# 为了保持向后兼容，保留原来的类名
CInstrument = Instrument




