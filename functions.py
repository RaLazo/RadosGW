# Title: RadosGW - Connector
# Eng.: Rafael Lazenhofer
# Ver.: 1.0
# Date: 21.12.2017

import boto
import boto.s3.connection


access_key = 'C8QE7PRORJGH4B52ZOZ7'
secret_key = 'VfuN9KgJaFfkL0POJbkVJ8FnpzaRgTHzowfj3Xy3'
# Connection zu rgw
conn = boto.connect_s3(
aws_access_key_id = access_key,
aws_secret_access_key = secret_key,
host = '192.168.1.3',
is_secure=False,
calling_format = boto.s3.connection.OrdinaryCallingFormat(),
)

def lists():
    for bucket in conn.get_all_buckets():
        print "{name}\t{created}".format(
                name = bucket.name,
                created = bucket.creation_date,
        ) 

def delete():
    print("Enter bucketname")
    bucketname=raw_input(">>> ")
    conn.delete_bucket(bucketname)

def create():
    print("Enter bucketname")
    bucketname=raw_input(">>> ")
    bucket = conn.create_bucket(bucketname)

def listobjects():
    print("Enter bucketname")
    bucketname=raw_input(">>> ")
    bucket = conn.get_bucket(bucketname)
    for key in bucket.list():
        print "{name}\t{size}\t{modified}".format(
                name = key.name,
                size = key.size,
                modified = key.last_modified,
                )

def switch(x):
    if x == 'l':
        lists()
    elif x =='d':
        delete()
    elif x == 'e':
        return 1
    elif x == 'h':
        h()
    elif x == 'c':
        create()
    elif x == 'lo':
        listobjects()
    #else:
        #print("there is not typo press h to get information")

def h():
    print("Choose Function")
    print ("- l, List your Buckets")
    print ("- d, Delete a Bucket")
    print ("- c, Create a Bucket")
    print ("- lo, a Bucket")
    print ("- h,help")
    print ("- e,exit")  