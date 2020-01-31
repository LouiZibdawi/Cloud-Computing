#!/usr/bin/env python
# coding: utf-8
#
# Example code to create a NoSQL DynamoDB table
#

from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

# Establish a connection to the AWS resource dynamodb

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

client = boto3.client('dynamodb')

# Create a new table called MovieInfo
try: 
    table = dynamodb.create_table(
        TableName='Movies',
        KeySchema=[
            {
                'AttributeName': 'year',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'  #Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'year',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print("Table status:", table.table_status, table.table_name)
except Exception as e:
    print(e)

waiter = client.get_waiter('table_exists')
waiter.wait(TableName='Movies')

table = dynamodb.Table('Movies')

with open("moviedata.json") as json_file:
    movies = json.load(json_file, parse_float = decimal.Decimal)
    for movie in movies:
        try:
            year = int(movie['year'])
            title = movie['title']
            info = movie['info']

            print("Adding movie:", year, title)

            table.put_item(
            Item={
                'year': year,
                'title': title,
                'info': info,
                }
            )
        except Exception as e:
            print('Failed to add ', title, ' due to ', e)
