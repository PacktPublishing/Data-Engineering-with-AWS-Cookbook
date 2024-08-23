from random import randint

def do_some_calculation(a):
  return randint(1, 10) + a

def get_config_value():
  with open('/tmp/my_config') as f:
    lines = f.readlines()
    return lines[0].strip()
