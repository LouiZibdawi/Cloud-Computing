#!/usr/bin/env python
# coding: utf-8

import boto3
import uuid

s3 = boto3.resource('s3')

def create_content():
    s3.create_bucket(Bucket="lzibdawi-cis1300")
    s3.Bucket('lzibdawi-cis1300').put_object(Key='lzibdawi-1300Assignment1.pdf', Body=open('/Users/louizibdawi/Documents/5-Winter/Cloud-Computing/data/lzibdawi-1300Assignment1.pdf', 'rb'))
    s3.Bucket('lzibdawi-cis1300').put_object(Key='lzibdawi-1300Assignment2.pdf', Body=open('/Users/louizibdawi/Documents/5-Winter/Cloud-Computing/data/lzibdawi-1300Assignment2.pdf', 'rb'))
    s3.Bucket('lzibdawi-cis1300').put_object(Key='lzibdawi-1300Assignment3.pdf', Body=open('/Users/louizibdawi/Documents/5-Winter/Cloud-Computing/data/lzibdawi-1300Assignment3.pdf', 'rb'))
    s3.Bucket('lzibdawi-cis1300').put_object(Key='lzibdawi-1300Assignment4.pdf', Body=open('/Users/louizibdawi/Documents/5-Winter/Cloud-Computing/data/lzibdawi-1300Assignment4.pdf', 'rb'))

    s3.create_bucket(Bucket="lzibdawi-cis3110")
    s3.Bucket('lzibdawi-cis3110').put_object(Key='lzibdawi-3110Lecture1.pdf', Body=open('/Users/louizibdawi/Documents/5-Winter/Cloud-Computing/data/lzibdawi-3110Lecture1.pdf', 'rb'))
    s3.Bucket('lzibdawi-cis3110').put_object(Key='lzibdawi-3110Lecture2.pdf', Body=open('/Users/louizibdawi/Documents/5-Winter/Cloud-Computing/data/lzibdawi-3110Lecture2.pdf', 'rb'))
    s3.Bucket('lzibdawi-cis3110').put_object(Key='lzibdawi-3110Lecture3.pdf', Body=open('/Users/louizibdawi/Documents/5-Winter/Cloud-Computing/data/lzibdawi-3110Lecture3.pdf', 'rb'))
    s3.Bucket('lzibdawi-cis3110').put_object(Key='lzibdawi-3110Assignment1.pdf', Body=open('/Users/louizibdawi/Documents/5-Winter/Cloud-Computing/data/lzibdawi-3110Assignment1.pdf', 'rb'))

    s3.create_bucket(Bucket="lzibdawi-cis4010")
    s3.Bucket('lzibdawi-cis4010').put_object(Key='lzibdawi-4010Lecture1.pdf', Body=open('/Users/louizibdawi/Documents/5-Winter/Cloud-Computing/data/lzibdawi-4010Lecture1.pdf', 'rb'))
    s3.Bucket('lzibdawi-cis4010').put_object(Key='lzibdawi-4010Lecture2.pdf', Body=open('/Users/louizibdawi/Documents/5-Winter/Cloud-Computing/data/lzibdawi-4010Lecture2.pdf', 'rb'))
    s3.Bucket('lzibdawi-cis4010').put_object(Key='lzibdawi-4010Assignment1.pdf', Body=open('/Users/louizibdawi/Documents/5-Winter/Cloud-Computing/data/lzibdawi-4010Assignment1.pdf', 'rb'))

if __name__ == "__main__":
    create_content()