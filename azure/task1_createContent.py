#!/usr/bin/env python
# coding: utf-8

import uuid, os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

# Create the BlobServiceClient object which will be used to create a container client
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

def create_content(containerName, blobs):
    try: 
        container_client = blob_service_client.create_container(containerName)
        print('Successfully created container: ' + containerName)
    except:
        print("Container already exists")

    for blobName in blobs:
        try:
            blob_client = blob_service_client.get_blob_client(container=containerName, blob=blobName)
            with open("/Users/louizibdawi/Documents/5-Winter/Cloud-Computing/data/" + blobName, "rb") as data:
                blob_client.upload_blob(data)
            print('Successfully created blob: ' + blobName)
        except:
            print('Blob already exists')


if __name__ == "__main__":
    create_content("lzibdawi-cis1300", ["lzibdawi-1300Assignment1.pdf", "lzibdawi-1300Assignment2.pdf", "lzibdawi-1300Assignment3.pdf", "lzibdawi-1300Assignment4.pdf"])
    create_content("lzibdawi-cis3110", ["lzibdawi-3110Lecture1.pdf", "lzibdawi-3110Lecture2.pdf", "lzibdawi-3110Lecture3.pdf", "lzibdawi-3110Assignment1.pdf"])
    create_content("lzibdawi-cis4010", ["lzibdawi-4010Lecture1.pdf", "lzibdawi-4010Lecture2.pdf", "lzibdawi-4010Assignment1.pdf"])