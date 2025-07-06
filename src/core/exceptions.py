"""
SimpleSCPI 项目的自定义异常类
"""

class SimpleSCPIError(Exception):
    """SimpleSCPI 基础异常类"""
    pass

class InstrumentError(SimpleSCPIError):
    """仪器相关异常"""
    pass

class ConnectionError(InstrumentError):
    """连接异常"""
    pass

class CommunicationError(InstrumentError):
    """通信异常"""
    pass

class ConfigurationError(SimpleSCPIError):
    """配置异常"""
    pass

class UIError(SimpleSCPIError):
    """UI相关异常"""
    pass
