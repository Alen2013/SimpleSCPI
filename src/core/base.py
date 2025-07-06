import os
from core.log_helper import LogHelper

class BaseObject:
    def __init__(self):
        self.execute_path = os.getcwd()
        self.logger = None

    def set_log(self, name, log_file):
        self.logger = LogHelper(name, log_file)
        
        '''
        #第一步，创建一个logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)  # Log等级总开关
        formatter = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)s] %(message)s")

        
        # 第二步，创建一个handler，用于写入日志文件
        date_path = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        #log_name = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        log_name = time.strftime('%Y%m%d', time.localtime(time.time()))
        log_path = os.path.dirname(os.getcwd()) + '/Logs/'+date_path+'/'
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        log_file = log_path + log_name + '.log'
        fh = logging.FileHandler(log_file, mode='w')
        fh.setLevel(logging.INFO)  # 输出到file的log等级的开关
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
      
        #创建一个handler，用于写入控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        '''
