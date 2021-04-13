import urllib3
import json
import base64
import logging
import datetime
from cprint import cprint

class Reporter:
  def __init__(self, url, interval, street):
    self.url = url
    self.http = urllib3.PoolManager()
    self.interval = interval
    self.street = street
    self.last_report_time = None

  def add_minutes(self, tm, minutes1):
    fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + datetime.timedelta(minutes=minutes1)
    return fulldate.time()

  def can_report(self):
    current_time = datetime.datetime.now().time()
    interval_time = current_time
    if self.last_report_time is not None:
      interval_time = self.add_minutes(self.last_report_time, int(self.interval))
    if interval_time > current_time:
      return False
    return True

  def report(self, filepath):
    if not self.can_report():
      cprint.info(f'not more then {self.interval} minutes')
      return

    logging.info("try to report from " + filepath)
    with open(filepath, 'rb') as fp:
      binary_data = fp.read()
      if not binary_data:
        cprint.err("read image err: " + filepath)
        return

      # not json, but form-data
      # data = {
      #   'images': [base64.encodebytes(binary_data).decode('utf-8')],
      #   "category": "测试",
      #   'street': self.street,
      #   'title': '告警'
      # }
      # encoded_data = json.dumps(data).encode('utf-8')
      # r = self.http.request(
      #   'POST',
      #   self.url,
      #   body=encoded_data,
      #   headers={'Content-Type': 'application/json'}
      # )

      r = self.http.request(
        'POST',
        self.url,
        fields={
          'event[images][]': ('image.jpg', binary_data),
          'event[title]': '告警',
          'event[street]': self.street,
          'event[category]': '测试'
        }
      )
      result = r.data
      logging.info("result: " + result.decode("utf-8"))
      self.last_report_time = datetime.datetime.now().time()