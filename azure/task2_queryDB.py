#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
import csv
import os
from azure.cosmos import CosmosClient, PartitionKey

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

primaryKey = None
primaryValue = None
primaryValueStart = None
primaryValueEnd = None
secondaryKey = None
secondaryValue = None
secondaryValueStart = None
secondaryValueEnd = None
filterName = None
filterExpression = None
filterValue = None
sort = None
fields = None
saveToCSV = None

def get_primary():
    global primaryKey, primaryValue, primaryValueStart, primaryValueEnd
    while 1==1:
        try:
            print("===================================================================")
            primaryKey = int(input('Primary/Partition Key [(1) Individual (2) Range (3) None]: '))
            print("===================================================================")
            if (primaryKey == 1):
                while 1==1:
                    try:
                        primaryValue = int(input('Individual year: '))
                        return
                    except ValueError:
                        print('[Invalid input. Must be a number]\n')
            elif primaryKey == 2:
                while 1==1:
                    try:
                        primaryValueStart = int(input('Start year: '))
                        primaryValueEnd = int(input('End year: '))
                        return
                    except ValueError:
                        print('[Invalid input. Must be a number]\n')
                return
            elif primaryKey == 3:
                primaryKey = None
                return
            else:
                print('[Invalid input. Must be a number from 1 to 3]\n')
        except ValueError:
            print('[Invalid input. Must be a number from 1 to 3]\n')

def get_secondary():
    global secondaryKey, secondaryValue, secondaryValueStart, secondaryValueEnd
    while 1==1:
        try:
            print("===================================================================")
            secondaryKey = int(input('Secondary/Sort Key [(1) Individual (2) Range (3) None]: '))
            print("===================================================================")
            if (secondaryKey == 1):
                while 1==1:
                    secondaryValue = input('Individual title: ')
                    return
            elif secondaryKey == 2:
                while 1==1:
                    secondaryValueStart = input('Start letter of range: ')
                    secondaryValueEnd = input('End letter of range: ')
                    # Input must be a single character
                    if (secondaryValueStart.isalpha() and len(secondaryValueStart) == 1 and secondaryValueEnd.isalpha() and len(secondaryValueEnd) == 1):
                        return
                    else:
                        print('[Invalid input. Must be a single character]\n')
                return
            elif secondaryKey == 3:
                secondaryKey = None
                return
            else:
                print('[Invalid input. Must be a number from 1 to 3]\n')
        except ValueError:
            print('[Invalid input. Must be a number from 1 to 3]\n')

def get_filters():
    global filterName, filterExpression, filterValue
    while 1==1:
        try:
            print("===================================================================")
            # Get filter name
            filterInput = int(input('Filter name [(1) rank, (2) rating, (3) runtime (4) None]: '))
            if filterInput == 1:
                filterName = 'info.rank'
            elif filterInput == 2:
                filterName = 'info.rating'
            elif filterInput == 3:
                filterName = 'info.running_time_secs'
            elif filterInput == 4:
                return
            else:
                print('[Invalid input. Must be a number from 1 to 4]\n')

            # Get filter expression and value
            if filterInput == 1 or filterInput == 2 or filterInput == 3:
                # Expression
                while 1 == 1:
                    try:
                        filterExpressionInput = int(input('Filter expression [(1) equal to (2) less than (3) greater than]: '))
                        if filterExpressionInput == 1:
                            filterExpression = 'eq'
                            break
                        elif filterExpressionInput == 2:
                            filterExpression = 'lt'
                            break
                        elif filterExpressionInput == 3:
                            filterExpression = 'gt'
                            break
                        else: 
                            print('[Invalid input. Must be a number from 1 to 3]\n')
                    except:
                        print('[Invalid input. Must be a number from 1 to 3]\n')
                # Value
                while 1 == 1:
                    try:
                        if (filterName == 'info.rating'):
                            filterValue = decimal.Decimal((input('Filter value (double): ')))
                        else:
                            filterValue = int(input('Filter value (integer): '))
                        return
                    except:
                        print('[Invalid input. Must be an integer/float]\n')    
        except:
            print('[Invalid input. Must be a number from 1 to 4]\n')

def get_sort():
    global sort
    while 1==1:
        try:
            print("===================================================================")
            sortInput = int(input('Sort [(1) Primary (2) Secondary (3) Other (4) None]: '))
            print("===================================================================")
            if (sortInput == 1):
                sort = "year"
                return
            elif sortInput == 2:
                sort = "title"
                return
            elif sortInput == 3:
                sort = input('Enter column to sort by: ')
                return
            elif sortInput == 4:
                sort = None
                return
            else:
                print('[Invalid input. Must be a number from 1 to 4]\n')
        except ValueError:
            print('[Invalid input. Must be a number from 1 to 4]\n')
        
def get_fields():
    global fields
    print("===================================================================")
    fields = input('Fields/Attributes [Separate by comma, leave blank for none]: ')
    if fields == '':
        fields = None
    print("===================================================================")

def get_save_to_csv():
    global saveToCSV
    print("===================================================================")
    while 1==1:
        try:
            saveToCSV = int(input('Save to CSV? [(0) no, (1) yes]: '))
            if saveToCSV == 0 or saveToCSV == 1:
                return
            else: 
                print('Invalid input. Must be 0 or 1]\n')
        except:
            print('Invalid input. Must be 0 or 1]\n')

    print("===================================================================")

def print_response(response):
    global fields, sort, saveToCSV
    # sort is either None, year, title or free text
    # open a file for writing

    try:
        if not response:
            print("There are no results to this query")
        else:
            if saveToCSV == 1:
                csvFile = open('./downloads/response.csv', 'w')
                csvwriter = csv.writer(csvFile, delimiter=",")
                headerRow = []
                # Write headers
                for attr, value, in response[0].items():
                    headerRow.append(str(attr))
                
                csvwriter.writerow(headerRow)
                # Write data
                for item in response:
                    row = []
                    for attr, value, in item.items():
                        row.append(str(value))
                    csvwriter.writerow(row)
                print("Successfully printed to CSV /downloads/response.csv")
            else:
                for item in response:
                    for attr, value, in item.items():
                        print(str(attr) + " - " + str(value))
    except Exception as e:
        print(e)
        print("Error printing items")

def query():
    global fields, primaryValue, primaryValueStart, primaryValueEnd, secondaryValue, secondaryValueStart, secondaryValueEnd, filterName, filterExpression, filterValue
    filtersEnabled = False
    if (fields):
        fields = fields.replace(",", ",c.")
        fields = "c." + fields
        query = "SELECT " + fields + " FROM c "
    else:
        query = "SELECT c.year, c.title FROM c "

    if primaryValue:
        query = query + "WHERE c.year=" + str(primaryValue) + " "
        filtersEnabled = True
    elif primaryValueStart:
        query = query + "WHERE (c.year BETWEEN " + str(primaryValueStart) + " AND " + str(primaryValueEnd) + ") "
        filtersEnabled = True
    
    if secondaryValue:
        if filtersEnabled == False:
            query = query + "WHERE c.title='" + str(secondaryValue) + "' "
            filtersEnabled = True
        else:
            query = query + "AND c.title='" + str(secondaryValue) + "' "
            filtersEnabled = True
    elif secondaryValueStart:
        if filtersEnabled == False:
            query = query + "WHERE (c.title BETWEEN '" + str(secondaryValueStart) + "' AND '" + str(secondaryValueEnd) + "') "
            filtersEnabled = True
        else:
            query = query + "AND (c.title BETWEEN " + str(secondaryValueStart) + " AND " + str(secondaryValueEnd) + "') "
        
    if filterName:
        if filterExpression == 'eq':
            if filtersEnabled == False:
                query = query + "WHERE c."+filterName+" = " + str(filterValue) + " "
                filtersEnabled = True
            else:
                query = query + "AND c."+filterName+" = " + str(filterValue) + " "
        elif filterExpression == 'gt':
            if filtersEnabled == False:
                query = query + "WHERE c."+filterName+" > " + str(filterValue) + " "
                filtersEnabled = True
            else:
                query = query + "AND c."+filterName+" > " + str(filterValue) + " "
        elif filterExpression == 'lt':    
            if filtersEnabled == False:
                query = query + "WHERE c."+filterName+" < " + str(filterValue) + " "
                filtersEnabled = True
            else:
                query = query + "AND c."+filterName+" < " + str(filterValue) + " "
    
    if sort:
        query = query + "ORDER BY c." + sort + " "

    try:
        items = list(table.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
            
        print("QUERY: " + query)
        print_response(items)
    except Exception as e:
        print(e)
        print('[Invalid query. Filters, sort or fields are incorrect]')


if __name__ == "__main__":
    get_primary()
    get_secondary()
    get_filters()
    get_sort()
    get_fields()
    get_save_to_csv()
    query()