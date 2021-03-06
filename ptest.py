import json
import os
import eventlet
import time

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def testWrap(f, input, timeout):
  def decorated(*args, **kwargs):
    args = input
    eventlet.monkey_patch()
    try:
        with eventlet.Timeout(timeout):
          return f(*args, **kwargs)
    except eventlet.timeout.Timeout:
        return 'function run timeout'
  return decorated

def testValidate(real, expect, option=""):
  if option != "" and real and type(real) == 'dict':
    return real[option] == expect[option]
  else:
    return real == expect


def ptest(func, funcPath, testcase):
  dict = {}
  # step1: read testcase
  with open(testcase, 'r') as f:
    dict = json.load(f)
  
  # step2: run tests
  funcTest = getattr(getattr(__import__(funcPath), 'solution'), func)

  # step3: generate tests results
  acc = 0
  length = len(dict['tests'])
  start = time.time()
  for test in dict['tests']:
    real = {}
    try:
      real = testWrap(funcTest,test['params'], dict['config']['timeout'])()
      assert testValidate(real, test['result'], test['option'])
    except AssertionError:
      print(WARNING+'----------',test['id']+1, '/', length,'---------'+ENDC)
      print('params: ', test['params'])
      print('expect:',test['result'])
      print(FAIL+'answer: ',real,ENDC)

    else:
      acc+=1
  
  print()
  print()
  print('-------------------')
  print('time cost', time.time() - start, 's')
  err = length - acc
  if err == 0:
    print('All Done!')
  else:
    print("Rate: ", acc / length, " , Acc: ",acc," , Err: ",(length-acc))

  return 0

cwd = os.getcwd()

ptest('mmsearch', 'mm-search.solution' ,cwd+'/mm-search/testcases.json')
