#!/usr/bin/env python
# coding: utf-8
#
# Example code to create a NoSQL DynamoDB table
#

from __future__ import print_function # Python 2/3 compatibility
from azure.cosmos import CosmosClient, PartitionKey
import boto3
import json
import decimal
import os

# Establish a connection to the AWS resource dynamodb
endpoint = os.getenv('AZURE_COSMOSDB_URI_STRING')
key = os.getenv('AZURE_COSMOSDB_PRIMARY_KEY_STRING')

client = CosmosClient(endpoint, key)

try:
    database_name = 'lzibdawi_cis4010'
    database = client.create_database_if_not_exists(id=database_name)
except Exception as e:
    print("Failed to create DB")

try: 
    table_name = 'Movies'
    table = database.create_container_if_not_exists(
        id=table_name, 
        partition_key=PartitionKey(path="/year"),
        offer_throughput=400
    )
except:
    print("Failed to create table")

with open("moviedata.json") as json_file:
    movies = json.load(json_file)
    id = 1
    for movie in movies:
        try:
            year = int(movie['year'])
            title = movie['title']
            info = movie['info']

            table.create_item(
            body={
                'id': str(id),
                'year': year,
                'title': title,
                'info': info,
                }
            )
            print("Added movie:", year, title)
            id = id + 1
        except Exception as e:
            print('Failed to add ', title, ' due to ', e)
