#!/usr/bin/env python

import re

config_file_name = './service_monitoring.conf'
parameters = {}

def ConfigParser(config_file_name):

  config_file = open(config_file_name, 'r')
  aws_params = []

  for i in config_file.read().splitlines():
    comment = re.compile('^#.*')
    if i and not comment.match(i):
      #print i
      if re.compile('^aws\..*').match(i):
#        print i
        aws_params.append(i)
      if re.compile('^namespace=.*').match(i):
        parameters.update(NameSpace(i))
#  AwsParamParser(aws_params)
  parameters.update(AwsParamParser(aws_params))
  return parameters

def NameSpace(line):
  return {"namespace":line.replace("namespace=", "")}

def AwsParamParser(params):
  key = ''
  private_key = ''
  for param in params:
    if re.compile('^aws.access.key=').match(param):
        key = param.replace("aws.access.key=", "")
#        print key
    elif re.compile('^aws.access.secret.key=.*').match(param):
      private_key = param.replace('aws.access.secret.key=', '')
#      print private_key
  return {"aws_access_keys":(key, private_key)}

if __name__ == '__main__':
  ConfigParser(config_file_name)
  print parameters
