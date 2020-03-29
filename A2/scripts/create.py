#!/usr/bin/env python
# coding: utf-8

import uuid, os
import json
import time
import subprocess
import boto3

ec2 = boto3.resource('ec2','us-east-1')
key_pair_name="ec2-1-keypair.pem"

################################
# SHARED FUNCTIONS
################################

def run_ssh(sshCommand, message, count):
  print('\nAttempting to connect to instance')
  success = os.system(sshCommand + " > /dev/null 2>&1")

  if success == 0:
    print('...succesfully ' + message + "\n")
  else:
    count = count + 1
    print('Failed to connect ['+str(count)+"]. Waiting 5 seconds and retrying..")
    if (count == 11):
      print('Failed to connect to instance 10 times. Aborting')
      return
    # Sleep for 5 seconds
    time.sleep(15)
    run_ssh(sshCommand, message, count)

################################
# AZURE
################################

def add_docker_azure(instanceData, instance):
  publicIP = instance['publicIpAddress']

  print("Installing docker...")
  installCommand = "\"sudo apt update && sudo apt install docker.io -y\""
  sshCommand = "ssh -o StrictHostKeyChecking=no " + publicIP + " " + str(installCommand) 
  run_ssh(sshCommand, "installed docker", 0)

  print("Starting docker...") 
  dockerCommand = "\"sudo service docker start\""
  sshCommand = "ssh -o StrictHostKeyChecking=no " + publicIP + " " + str(dockerCommand) + " "
  run_ssh(sshCommand, "started docker", 0)

  count = 0;
  for image in instanceData['docker']:
    if count == 0:
      imageCommand = "sudo docker pull " + image['name']
    else:
      imageCommand = imageCommand + " && sudo docker pull " + image['name']

    if image['background'] == 'Y':
        imageCommand = imageCommand + " && sudo docker run " + image['name']
    count = count + 1
  
  if (count > 0):
    print("Adding docker images...")
    sshCommand = "ssh -o StrictHostKeyChecking=no " + publicIP + " \"" + str(imageCommand) + "\""
    run_ssh(sshCommand, "added docker images", 0)

def create_instance_azure(instanceData):
  createResource = "az group create --name Resources --location eastus"
  resource = subprocess.run(createResource, shell=True, capture_output=True)

  createInstance = "az vm create --resource-group Resources \
  --name " + instanceData['instance_name'] + " \
  --image " + instanceData['image'] + " \
  --generate-ssh-keys \
  --output json \
  --verbose "

  response = subprocess.run(createInstance, shell=True, capture_output=True)
  
  decodedResponse = response.stdout.decode('utf-8')
  instance = json.loads(decodedResponse)

  print('...successfully created instance\n')
  
  if 'docker' in instanceData:
    add_docker_azure(instanceData, instance)


################################
# AWS
################################

def add_docker_aws(instanceData, instance):
  instance.wait_until_running()
  
  instance = ec2.Instance(id=instance.id)
  sshUser = instanceData['ssh_user']

  installCommand = ""
  if instanceData['vm'] == "ubuntu" or instanceData['vm'] == "amazon-linux":
    if instanceData['vm'] == "ubuntu":
      installCommand = "\"sudo apt update && sudo apt install docker.io -y\""
    else: 
      installCommand = "\"sudo yum install docker -y\""
  
    print("Installing docker...")
    sshCommand = "ssh -o StrictHostKeyChecking=no -i " + str(key_pair_name) + " " + str(sshUser) + "@" + str(instance.public_dns_name) + " " + str(installCommand) 
    run_ssh(sshCommand, "installed docker", 0)

  print("Starting docker...") 
  dockerCommand = "\"sudo service docker start\""
  sshCommand = "ssh -o StrictHostKeyChecking=no -i " + str(key_pair_name) + " " + str(sshUser) + "@" + str(instance.public_dns_name) + " " + str(dockerCommand) + " "
  run_ssh(sshCommand, "started docker", 0)

  count = 0;
  for image in instanceData['docker']:
    if count == 0:
      imageCommand = "sudo docker pull " + image['name']
    else:
      imageCommand = imageCommand + " && sudo docker pull " + image['name']

    if image['background'] == 'Y':
        imageCommand = imageCommand + " && sudo docker run " + image['name']
    count = count + 1
  
  if (count > 0):
    print("Adding docker images...")
    sshCommand = "ssh -o StrictHostKeyChecking=no -i " + str(key_pair_name) + " " + str(sshUser) + "@" + str(instance.public_dns_name) + " \"" + str(imageCommand) +"\""
    run_ssh(sshCommand, "added docker images", 0)


def create_instance_aws(instanceData):
  try:
    instances = ec2.create_instances(
      ImageId=instanceData['ami'],
      MinCount=1,
      MaxCount=1,
      InstanceType=instanceData['instance_type'],
      KeyName='ec2-1-keypair',
      TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': instanceData['instance_name']
                },
            ]
        },
      ],
    )
    print('...successfully created instance\n')
    
    if 'docker' in instanceData:
      add_docker_aws(instanceData, instances[0])
  except Exception as e:
    print('Failed to create instance ' + instanceData['ami'])
    print(e)

################################
# SHARED FUNCTIONS
################################

def readDataFile():
  with open('../data/config.json') as json_file:
    data = json.load(json_file)
    # Loop through containers
    for instance in data['instances']:
      print('=================================================')
      print('Creating instance: ', instance['instance_name'])
      print('On: ' + instance['platform'])
      print('=================================================')

      if instance['platform'] == 'aws':
        create_instance_aws(instance)
      else:
        create_instance_azure(instance)

if __name__ == '__main__':
    readDataFile()