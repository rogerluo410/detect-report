import sys
import json
import yaml
import os
import logging

from cprint import cprint
from modules.run import GoThread
from modules.detect import detect
from modules.report import Reporter

def main():

  with open('./config.yaml') as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)  # Read config
    if config:
      cprint.ok("load config is " + json.dumps(config))
    else:
      cprint.info("load config file `config.yaml` failed")

  # Set logger
  logging.basicConfig(
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("./log/detect.log"),
        logging.StreamHandler()
    ]
  )

  # Get environment variables
  source = os.environ.get('DETECT_SOURCE') or config.get("source")
  keys = config.get("keys")
  if os.environ.get('DETECT_KEYS') is not None:
    keys = os.environ.get('DETECT_KEYS').split(",")
  street = os.environ.get('DETECT_STREET') or config.get("street")
  interval = os.environ.get('DETECT_INTERVAL') or config.get("interval")
  device = os.environ.get('DETECT_DEVICE') or config.get("device")
  report_url = os.environ.get('REPORT_URL') or config.get("report_url")

  # Run detect
  reporter = Reporter(report_url, interval, street)
  detect(source, device, keys, reporter)

  # threads = []
  # for source in config.get("sources"):
  #   t = GoThread("Thread for "+source, source, config.get("device"))
  #   t.start()
  #   threads.append(t)
  
  # # 等待所有线程完成
  # for t in threads:
  #   t.join()

if __name__ == "__main__":
  main()