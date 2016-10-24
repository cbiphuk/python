#!/usr/bin/python2.7


import os.path
import httplib
import datetime

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

  #date = '{:%Y-%m-%dT%H:%M:%S}'.format(datetime.datetime.now())

  conn = httplib.HTTPConnection(webservice_url, 80)
  try:
    conn.request("HEAD", "/")
  except:
    log_message = 'is not responding'
    PushLog(service_name, log_message)
    #print date + ': '+ webservice_name + ' is not responding'
    return (service_name, False)
  else:
    r1 = conn.getresponse()
    log_message = 'is alive ' + str(r1.status) + ' ' + r1.reason
    PushLog(service_name, log_message)
    #print date + ': ' + service_name + ' is alive ' + str(r1.status), r1.reason
    return (service_name, True)

def IsAlive(pid_file, service_name, system_name):
  """ This function checks of process status and tries to restart it if the process does not launched"""

  #date = '{:%Y-%m-%dT%H:%M:%S}'.format(datetime.datetime.now())
  if os.path.isfile(pid_file):
    log_message = 'pis is over there'
    PushLog(service_name, log_message)
    #print date + ': ' + service_name + " pid is over there"
    the_file = open(pid_file, 'r')
    pid = the_file.readline()
    try:
      os.kill(int(pid), False)
      log_message = 'process is running'
      PushLog(service_name, log_message)
      #print date + ': ' + service_name + " process is running"
      return (service_name, True)
    except:
      log_message = 'pid file exist but process is dead'
      PushLog(service_name, log_message)
      #print date + ': ' + service_name + " pid file exist but process is dead"
      serviceRestart(system_name)
      return (service_name, False)
  else:
    log_message = 'is DEAD!'
    PushLog(service_name, log_message)
    #print date + ': ' + service_name + " is DEAD!"
    serviceRestart(system_name)
    return (service_name, False)

def AWSSendStatus(service):
  """Sends status of current process to AWS Cloudwatch.
  """
  #TODO: use aws api instead of aws-cli
  
  status = service[1]
  service_name = service[0]
  #date = '{:%Y-%m-%dT%H:%M:%S}'.format(datetime.datetime.now())

  if status:
    value = 1
    command = '/usr/local/bin/aws cloudwatch put-metric-data --metric-name ' \
    + service_name + ' --namespace ' + namespace + ' --value ' + str(value) + \
    ' --timestamp '+ GetDate()
    #print command
  else:
    value = 0
    command = '/usr/local/bin/aws cloudwatch put-metric-data --metric-name ' \
    + service_name + ' --namespace ' + namespace + ' --value ' + str(value) + \
    ' --timestamp '+ GetDate()
    #print command
  os.system(command)

def serviceRestart(service_name):
  """Restarts current service"""

  #date = '{:%Y-%m-%dT%H:%M:%S}'.format(datetime.datetime.now())
  command = 'sudo service ' + service_name + ' restart'
  log_message = 'restarting'
  PushLog(service_name, log_message)
  #print GetDate() + ': ' + service_name + ' restarting'
  os.system(command)

def PushLog(service_name, message):
  #date = '{:%Y-%m-%dT%H:%M:%S}'.format(datetime.datetime.now())
  print GetDate() + ': ' + service_name + ' ' + message

def GetDate():
  date = '{:%Y-%m-%dT%H:%M:%S}'.format(datetime.datetime.now())
  return date



#MAIN
if __name__ == '__main__':
  AWSSendStatus(IsAlive(nginx_pid, nginx_name, nginx_system_name))
  AWSSendStatus(IsAlive(php_fpm_pid, php_fpm_name, php_fpm_system_name))
  AWSSendStatus(IsAlive(mysql_pid, mysql_service_name, mysql_system_name))
  AWSSendStatus(WebserviceChecker(webservice_name, webservice_url))
