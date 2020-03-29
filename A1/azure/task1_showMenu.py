#!/usr/bin/env python
# coding: utf-8

import uuid, os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

# Create the BlobServiceClient object which will be used to create a container client
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

def display_all():
    try:
        all_containers = blob_service_client.list_containers(include_metadata=True)
        for container in all_containers:
            print(container['name'])
            container_client = ContainerClient.from_connection_string(connect_str, container_name=container['name'])
            blob_list = container_client.list_blobs()
            for blob in blob_list:
                print("\t" + blob.name)
    except Exception as s:
        print(s)

def download_object():
    print('Enter container name: ')
    containerName = input()
    print()

    print('Enter object name: ')
    objName = input()
    print()

    try:
        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=containerName, blob=objName)

        with open('downloads/' + objName, 'wb') as file:
	        file.write(blob_client.download_blob().readall())

        print("...successfully downloaded!")
    except:
        if os.path.exists('./downloads/' + objName):
            os.remove('./downloads/' + objName)
        
        print("Could not download")

def display_in_bucket():
    print('Enter container name: ')
    containerName = input()
    print()

    try:
        container_client = ContainerClient.from_connection_string(connect_str, container_name=containerName)
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            print("\t" + blob.name)
    except:
        print("Container does not exist")

def display_object():
    print('Enter object name: ')
    objName = input()
    print()

    found = 0;
    try:
        all_containers = blob_service_client.list_containers(include_metadata=True)
        for container in all_containers:
            container_client = ContainerClient.from_connection_string(connect_str, container_name=container['name'])
            blob_list = container_client.list_blobs()
            for blob in blob_list:
                if (blob.name == objName):
                    found = 1
                    print('Exists in container: ', container['name'])
    except:
        print("Object does not exist")

    if (found == 0):
        print('Object does not exist')

def process_option(option): 
    if option == 1:
        display_all()
    elif option == 2:
        display_in_bucket()
    elif option == 3:
        display_object()
    elif option == 4:
        download_object()
    elif option == 5:
        exit()


def show_menu():
    print('\n=================================')
    print('Select one the following options:')
    print('=================================')
    print('1. Display objects in all containers')
    print('2. Display objects in specific container')
    print('3. Display object with a specific name')
    print('4. Download object by name')
    print('5. Exit')
    print('=================================')
    option = int(input())
    print()
    process_option(option)
    

if __name__ == "__main__":
    while 1==1:
        show_menu()
