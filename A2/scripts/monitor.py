from __future__ import print_function # Python 2/3 compatibility
import boto3
import os
import time
import subprocess
import json

ec2 = boto3.resource('ec2','us-east-1')
key_pair_name="ec2-1-keypair.pem"

def run_ssh(sshCommand):
  # Get List of installed docker images
  cmd = sshCommand + " sudo docker image ls"
  process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()
  print("Docker Images: ")
  print(output.decode('UTF-8'))

  cmd = sshCommand + " sudo docker ps -a"
  process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()
  print("Docker Containers: ")
  print(output.decode('UTF-8')) 

def monitorAWS():
  print('=================================')
  print('        Monitoring AWS')
  print('=================================')
  instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

  count = 0
  for instance in instances:
    print("*** VM: " + instance.id + " ****")
    print(instance.id)

    sshCommand = 'ssh -o StrictHostKeyChecking=no -i ' + key_pair_name \
        + " ec2-user@" + instance.public_dns_name

    print(instance.id)
    # Ubuntu 
    if instance.id == 'i-0711f7a487a0080d9':
      sshCommand = 'ssh -o StrictHostKeyChecking=no -i ec2-1-keypair.pem ' \
        + "ubuntu@" + instance.public_dns_name
    else:
      sshCommand = 'ssh -o StrictHostKeyChecking=no -i ec2-1-keypair.pem ' \
        + "ec2-user@" + instance.public_dns_name

    run_ssh(sshCommand)
    count = count + 1

  if count == 0:
    print('No instances are running\n')

def monitorAzure():
  print('=================================')
  print('       Monitoring Azure')
  print('=================================')
  instanceList = "az vm list -d"
  response = subprocess.run(instanceList, shell=True, capture_output=True)
  
  decodedResponse = response.stdout.decode('utf-8')
  instances = json.loads(decodedResponse)
  if len(instances) == 0:
    print('No instances are running')
  else:
    for instance in instances:
      print("*** VM: " + instance['name'] + " ***")
      sshCommand = "ssh -o StrictHostKeyChecking=no " + instance['publicIps'] + " "
      run_ssh(sshCommand)

if __name__ == '__main__':
  monitorAWS()
  monitorAzure()
