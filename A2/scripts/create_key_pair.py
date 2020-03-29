import boto3

ec2 = boto3.resource('ec2','us-east-1')

outfile = open('ec2-1-keypair.pem','w')

key_pair = ec2.create_key_pair(KeyName='ec2-1-keypair')

KeyPairOut = str(key_pair.key_material)
print(KeyPairOut)
outfile.write(KeyPairOut)