#!/usr/bin/env python

from boto.ec2.cloudwatch import CloudWatchConnection
import os.path
import httplib
import datetime
import configparser

config_file_name = 'service_monitoring.conf'

#TODO: add enable_monitoring feature
enable_monitoring = True


def WebserviceChecker(service_name, url):
  """ Checks webservice for current URL"""


  conn = httplib.HTTPConnection(url, 80, timeout = 10)
  try:
    conn.request("HEAD", "/")
  except:
    log_message = 'is not responding'
    PushLog(service_name, log_message)
    return (service_name, False)
  else:
    r1 = conn.getresponse()
    log_message = 'is alive ' + str(r1.status) + ' ' + r1.reason
    PushLog(service_name, log_message)
    return (service_name, True)

def IsAlive(pid_file, service_name, system_name):
  """ This function checks process status and tries to restart it if the
  process is not launched"""

  if os.path.isfile(pid_file):
    log_message = 'pid is over there'
    PushLog(service_name, log_message)
    the_file = open(pid_file, 'r')
    pid = the_file.readline()
    try:
      os.kill(int(pid), False)
      log_message = 'process is running'
      PushLog(service_name, log_message)
      return (service_name, True)
    except:
      log_message = 'pid file exist but process is dead'
      PushLog(service_name, log_message)
      serviceRestart(system_name)
      return (service_name, False)
  else:
    log_message = 'is DEAD!'
    PushLog(service_name, log_message)
    serviceRestart(system_name)
    return (service_name, False)

def AWSSendStatus(service):
  """Sends status of current process to AWS Cloudwatch.
  """
  #TODO: use aws api instead of aws-cli
  
  status = service[1]
  service_name = service[0]

  if status:
    value = 1
    command = '/usr/local/bin/aws cloudwatch put-metric-data --metric-name ' \
    + service_name + ' --namespace ' + namespace + ' --value ' + str(value) + \
    ' --timestamp '+ GetDate()
  else:
    value = 0
    command = '/usr/local/bin/aws cloudwatch put-metric-data --metric-name ' \
    + service_name + ' --namespace ' + namespace + ' --value ' + str(value) + \
    ' --timestamp '+ GetDate()
  os.system(command)

def serviceRestart(service_name):
  """Restarts current service"""

  command = 'sudo service ' + service_name + ' restart'
  log_message = 'restarting'
  PushLog(service_name, log_message)
  os.system(command)

def PushLog(service_name, message):
  print GetDate() + ': ' + service_name + ' ' + message

def GetDate():
  date = '{:%Y-%m-%dT%H:%M:%S}'.format(datetime.datetime.now())
  return date

def AWSSendStatusSDK(service):
  """Send status to AWS using SDK
  pip install boto"""
  status = service[1]
  service_name = service[0]

  cwc = CloudWatchConnection(aws_access_key_id, \
      aws_secret_access_key)
  if status:
    value = 1
  else:
    value = 0

  cwc.put_metric_data(namespace, name = service_name, value = str(value))

def ServiceSendStatus(parameters):
  services = parameters["services"]
  for keys, value in services.items():
    pid = value[0]
    name = value[1]
    system_name = value[2]

    AWSSendStatusSDK(IsAlive(pid, name, system_name))

def WebServiceSendStatus(parameters):
  services = parameters["webservices"]
  for keys, value in services.items():
    webservice_name = value[0]
    webservice_url = value[1]
    AWSSendStatusSDK(WebserviceChecker(webservice_name, webservice_url))

#MAIN
if __name__ == '__main__':
  parameters = configparser.ConfigParser(config_file_name)
  namespace = parameters["namespace"]
  aws_access_key_id = parameters["aws_access_keys"][0]
  aws_secret_access_key = parameters["aws_access_keys"][1]
  ServiceSendStatus(parameters)
  WebServiceSendStatus(parameters)
