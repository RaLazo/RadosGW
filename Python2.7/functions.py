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
host = '172.16.136.3',
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
    bn=bn()
    conn.delete_bucket(bucketname)

def create():
    bn=bn()
    bucket = conn.create_bucket(bn)

def bn():
    print("Enter bucketname")
    bn=raw_input(">>> ")
    return bn

def listobjects(bucketname):
    bucket = conn.get_bucket(bucketname)
    for key in bucket.list():
        print "{name}\t{size}\t{modified}".format(
                name = key.name,
                size = key.size,
                modified = key.last_modified,
                )


def switch(x):
    y=x.split()
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
    elif len(x.split())>1:
        if y[0]=='lo':
             listobjects(y[1])
    elif len(x.split())>1:
        if y[0]=='mo':
    #else:
        #print("is not a typo press h to get information")

def h():
    print("Choose Function")
    print ("- l, list your buckets")
    print ("- d, delete a bucket")
    print ("- c, create a bucket")
    print ("- lo, list objects of an bucket")
    print ("- mo. make an object => bucket")
    print ("- h,help")
    print ("- e,exit")  