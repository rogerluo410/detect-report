import threading
from cprint import cprint
from modules.detect import detect

class GoThread (threading.Thread):
  def __init__(self, threadID, source, device):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.source = source
      self.device = device
  def run(self):
      cprint.info("开启线程：" + self.threadID)
      detect(self.source, self.device)
      cprint.info ("退出线程：" + self.threadID)