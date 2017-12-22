# title: RGW - Connector
# eng.: Rafael Lazenhofer
# ver.: 1.0
#date : 22.12.2017
#import boto
#import boto.S3.connection
#access_key = 'C8QE7PRORJGH4B52ZOZ7'
#secret_key = 'VfuN9KgJaFfkL0POJbkVJ8FnpzaRgTHzowfj3Xy3'
def switch(x):
    "This is a switch function to check which part should be used"
    if x == 'l':
        lists()
    elif x == 'd':
        delete()
    elif x == 'c':
        create()
    elif x == 'e':
        i = 1
    return i

#conn = boto.connect_s3(
#        aws_access_key_id = access_key,
#        aws_secret_access_key = secret_key,
#        host = 'objects.dreamhost.com',
#        is_secure=False,               # uncomment if you are not using ssl
#        calling_format = boto.s3.connection.OrdinaryCallingFormat(),
#        )

i = 0
while i == 0:
    print (" RGW - Connector")
    print ("- l,List your Buckets")
    print ("- d,Delete a Bucket")
    print ("- c,Create a Bucket")
    print ("- e,exit")
    x=raw_input(">>> ")
    n=switch(x)
    if n == 1:
        i += 1
s