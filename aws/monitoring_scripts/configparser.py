#!/usr/bin/env python

import re

config_file_name = './service_monitoring.conf'
parameters = {}
services = []
webservices = []
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
      if re.compile('^service').match(i):
        services.append(i)
      if re.compile('^webservice').match(i):
        webservices.append(i)
#  AwsParamParser(aws_params)
  parameters.update(AwsParamParser(aws_params))
  parameters.update(AwsServiceParamsParser(services))
  #AwsServiceParamsParser(services)
  parameters.update(AwsWebServiceParamsParser(webservices))
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

def AwsWebServiceParamsParser(services):
  web_service_collection = {}
  for web_service in services:
    web_service_name = re.sub("\..*","", web_service.replace("webservice.",""))
    #print web_service_name
    web_service_collection[web_service_name] = [None,None]
  #print web_service_collection
  for web_service in services:
    position = 0
    web_service_name = re.sub("\..*","", web_service.replace("webservice.",""))
    web_service_param = re.sub("=.*$", "", re.sub("^webservice\.[a-z]*\.","", web_service))
    web_service_param_value = re.sub("^.*=", "", web_service)
    #print service_name, service_param, service_param_value
    if web_service_param == 'name':
      position = 0
    if web_service_param == 'url':
      position = 1
    web_service_parameters = web_service_collection.get(web_service_name)
    web_service_parameters[position] = web_service_param_value
    web_service_collection[web_service_name] = web_service_parameters
  #print web_service_collection
  return {"webservices":web_service_collection}


def AwsServiceParamsParser(services):
  service_collection = {}
  for service in services:
    service_name = re.sub("\..*","", service.replace("service.",""))
    service_collection[service_name] = [None,None,None]
#  print service_collection
  for service in services:
    position = 0
    service_name = re.sub("\..*","", service.replace("service.",""))
    service_param = re.sub("=.*$", "", re.sub("^service\.[a-z]*\.","", service))
    service_param_value = re.sub("^.*=", "", service)
    #print service_name, service_param, service_param_value
    if service_param == 'pid':
      position = 0
    if service_param == 'name':
      position = 1
    if service_param == 'systemname':
      position = 2
    service_parameters = service_collection.get(service_name)
    service_parameters[position] = service_param_value
    service_collection[service_name] = service_parameters
  #print service_collection
  return {"services":service_collection}


if __name__ == '__main__':
  ConfigParser(config_file_name)
  print parameters
  #print services
