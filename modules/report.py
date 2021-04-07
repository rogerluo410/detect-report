import urllib3
import json
from cprint import cprint

class Reporter:
  def __init__(self, url):
    self.url = url

  def report(self, filepath):
    with open(filepath, 'rb') as fp:
      binary_data = fp.read()
      if not binary_data:
        cprint.err("read image err: " + filepath)
        return

      r = http.request(
        'POST',
        self.url,
        body=binary_data,
        headers={'Content-Type': 'image/jpeg'}
      )
    json.loads(r.data.decode('utf-8'))['files']
