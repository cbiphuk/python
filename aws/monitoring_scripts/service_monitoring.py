#!/usr/bin/env python

from boto.ec2.cloudwatch import CloudWatchConnection
import os.path
import httplib
import datetime
import configparser

config_file_name = 'service_monitoring.conf'

#AWS namespace
namespace = ''
#TODO: add enable_monitoring feature
enable_monitoring = True

#nginx config
nginx_pid = '/var/run/nginx.pid'
nginx_name = 'NginxService'
nginx_system_name = 'nginx'

#php config
php_fpm_pid = '/var/run/php/php7.0-fpm.pid'
php_fpm_name = 'PhpFpmService'
php_fpm_system_name = 'php7.0-fpm'

#mysql config
mysql_pid = '/var/run/mysqld/mysqld.pid'
mysql_service_name = 'MysqlService'
mysql_system_name = 'mysql'

#webservice checker
webservice_name = 'WebService'
webservice_url = 'example.com'

def WebserviceChecker(service_name, url):
  """ Checks webservice for current URL"""


  conn = httplib.HTTPConnection(webservice_url, 80)
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

#def SetConfigValues(config_file_name):
#  parameters = configparser.ConfigParser(config_file_name)
#  namespace = parameters["namespace"]
#  #print namespace


#MAIN
if __name__ == '__main__':
  #iSetConfigValues(config_file_name)
  parameters = configparser.ConfigParser(config_file_name)
  namespace = parameters["namespace"]
  aws_access_key_id = parameters["aws_access_keys"][0]
  aws_secret_access_key = parameters["aws_access_keys"][1]
  #print aws_access_key_id, aws_secret_access_key
  #exit(0)

  AWSSendStatusSDK(IsAlive(nginx_pid, nginx_name, nginx_system_name))
  AWSSendStatusSDK(IsAlive(php_fpm_pid, php_fpm_name, php_fpm_system_name))
  AWSSendStatusSDK(IsAlive(mysql_pid, mysql_service_name, mysql_system_name))
  AWSSendStatusSDK(WebserviceChecker(webservice_name, webservice_url))
  #print configparser.ConfigParser(config_file_name)
  #print namespace
