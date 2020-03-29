Assignment 2, Feb 23rd, 2019

Loui Zibdawi

0924538

---

## Set up AWS environment

Add credentials to:
`~/.aws/credentials`

Add region to:
`~/.aws/config`

Create key pair for AWS:

```
cd scripts
python create_key_pair.py
```

---

## Description

- This program is a one-click deployment of VM's to AWS and/or Azure. The set up for the VM's is included in a config file in JSON format.
- There is a monitoring script that will show the VM's that are running as well as their docker images and containers running on them

---

## Configuration

- Each VM that is made requires a configuration to be filled out prior. Examples of AWS and Azure configurations are included below

_AWS_

```
{
  "platform": "aws",
  "instance_name": "aws-instance-amazon-linux-02",
  "ami": "ami-0a887e401f7654935",
  "instance_type": "t2.micro",
  "vm": "amazon-linux",
  "docker": [
    {
      "name": "golang",
      "background": "Y"
    },
    {
      "name": "gcc",
      "background": "Y"
    }
  ],
  "ssh_user": "ec2-user"
},
```

_AZURE_

```
{
  "platform": "azure",
  "instance_name": "azure-instance-ubuntu-18.04",
  "image": "UbuntuLTS",
  "docker": [
    {
      "name": "golang",
      "background": "Y"
    },
    {
      "name": "gcc",
      "background": "Y"
    }
  ]
},
```

---

## One click deploy

```
cd scripts
python create.py
```

---

## Monitoring

```
cd scripts
python monitor.py
```

---

## Notes:

- Redhat is not supported
