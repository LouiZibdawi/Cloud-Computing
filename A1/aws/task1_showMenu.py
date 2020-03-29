#!/usr/bin/env python
# coding: utf-8

import boto3

s3 = boto3.resource('s3')

def display_all():
    for bucket in s3.buckets.all():
        print(bucket.name)
        for obj in bucket.objects.all():
            print('\t' + obj.key)

def download_object():
    print('Enter container name: ')
    bucketName = input()
    print()

    print('Enter object name: ')
    objName = input()
    print()

    try:
        with open('downloads/' + objName, 'wb') as file:
            s3.Bucket(bucketName).download_fileobj(objName, file)

        print("...successfully downloaded!")
    except:
        print("Could not download")

def display_in_bucket():
    print('Enter container name: ')
    bucketName = input()
    print()

    try:
        bucket = s3.Bucket(bucketName)
        print('Objects in ' + bucketName + ':')
        for obj in bucket.objects.all():
            print(obj.key)
    except:
        print("Bucket does not exist")

def display_object():
    print('Enter object name: ')
    objName = input()
    print()
    found = 0;
    try:
        for bucket in s3.buckets.all():
            for obj in bucket.objects.all():
                if obj.key == objName:
                    found = 1
                    print('Exists in bucket: ', bucket.name)
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
