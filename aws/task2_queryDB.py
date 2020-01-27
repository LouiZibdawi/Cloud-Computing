#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
import csv
from boto3.dynamodb.conditions import Key, Attr, And

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

table = dynamodb.Table('Movies')

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

def sort_and_filter_response(response):
    global fields, sort, saveToCSV
    # sort is either None, year, title or free text
    # open a file for writing

    try:
        if sort is None:
            sortedResponse = response['Items']
        elif 'info.' in sort:
            sortedResponse = sorted(response['Items'], key=lambda k: k['info'].get(sort.replace('info.', ''), 0), reverse=True)
        elif sort == 'year' or sort == 'title':
            sortedResponse = sorted(response['Items'], key=lambda k: k.get(sort, 0), reverse=True)
        else:
            print('[Invalid query. Incorrect sort]')
    except:
        print('[Invalid query. Incorrect sort]')

    if fields != None:
        fields = [field.strip() for field in fields.split(',')]
    
    try:
        if saveToCSV == 1:
            csvFile = open('./downloads/response.csv', 'w')
            csvwriter = csv.writer(csvFile, delimiter=",")
            row = []
            if fields != None:
                for field in fields:
                    if 'info.' in field:
                        row.append(field.replace('info.', ''))
                    else:
                        row.append(field)
            else:
                row.append('title')
                row.append('year')
            csvwriter.writerow(row)

        for i in sortedResponse:
            if fields != None:
                row = []
                for field in fields:
                    if 'info.' in field:
                        try:
                            infoField = field.replace('info.', '')
                            if saveToCSV == 1:
                                row.append(i['info'][infoField])
                            else:
                                print(infoField, ', ',  i['info'][infoField])
                        except Exception as e:
                            if saveToCSV == 1:
                                row.append(infoField)
                                csvwriter.writerow(row)
                            else:
                                print(infoField, ' -    --------------')
                    else: 
                        if saveToCSV == 1:
                            row.append(i[field])
                        else:
                            print(field, ' - ', i[field])

                csvwriter.writerow(row)
            else:
                if saveToCSV == 1:
                    row = []
                    row.append(i['title'])
                    row.append(i['year'])
                    csvwriter.writerow(row)
                else:
                    print ( "title - ", i['title'])
                    print ( "year -", i['year'])
    except Exception as e:
        print(e)
        print('[Inproper query. Fields may not exist]')
    

def query():
    try:
        if primaryValue:
            fe = Key('year').eq(primaryValue)
        elif primaryValueStart:
            fe = Key('year').between(primaryValueStart, primaryValueEnd)
        else:
            fe = None
        
        if secondaryValue:
            if fe is None:
                fe = Key('title').eq(secondaryValue)
            else:
                fe = And(fe, Key('title').eq(secondaryValue))
        elif secondaryValueStart:
            if fe is None:
                fe = Key('title').between(secondaryValueStart, secondaryValueEnd)
            else:
                fe = And(fe, Key('title').between(secondaryValueStart, secondaryValueEnd))
            
        if filterName:
            if filterExpression == 'eq':
                if fe is None:
                    fe = Attr(filterName).eq(filterValue)
                else:
                    fe = And(fe, Attr(filterName).eq(filterValue))
            elif filterExpression == 'gt':
                if fe is None:
                    fe = Attr(filterName).gt(filterValue)
                else: 
                    fe = And(fe, Attr(filterName).gt(filterValue))
            elif filterExpression == 'lt':    
                if fe is None:
                    fe = Attr(filterName).lt(filterValue)
                else:   
                    fe = And(fe, Attr(filterName).lt(filterValue))
            
        if fe is None:
            response = table.scan()
        else: 
            response = table.scan(FilterExpression=fe)
        
        sort_and_filter_response(response)
    except Exception as e:
        print(e)
        print('[Invalid query. Filters are incorrect]')


if __name__ == "__main__":
    get_primary()
    get_secondary()
    get_filters()
    get_sort()
    get_fields()
    get_save_to_csv()
    query()