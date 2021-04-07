import sys
import json
import yaml
from cprint import cprint

def main():

  with open('./config.yaml') as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)  # Read config
    if config:
      cprint.ok("load config is " + json.dumps(config))
    else:
      cprint.fatal("load config file `config.yaml` failed")
  
  

if __name__ == "__main__":
  main()