# Title: RadosGW - Connector
# Eng.: Rafael Lazenhofer
# Ver.: 1.0
# Date: 21.12.2017

import math, os
import boto
import boto.s3.connection
from boto.s3.key import Key
from filechunkio import FileChunkIO

access_key = 'C8QE7PRORJGH4B52ZOZ7'
secret_key = 'VfuN9KgJaFfkL0POJbkVJ8FnpzaRgTHzowfj3Xy3'
server = '172.16.136.3'
# Connection zu rgw
conn = boto.connect_s3(
aws_access_key_id = access_key,
aws_secret_access_key = secret_key,
host = server,
is_secure=False,
calling_format = boto.s3.connection.OrdinaryCallingFormat(),
)

def lists():
    for bucket in conn.get_all_buckets():
        print ("{name}\t{created}".format(
                name = bucket.name,
                created = bucket.creation_date,
        ))

def delete(bn):
    bucketname = conn.get_bucket(bn)
    for key in bucketname:
        key.delete()
    conn.delete_bucket(bucketname)

def create(bn):
    bucket = conn.create_bucket(bn)

#def bn():
#    print("Enter bucketname")
#    bn=input(">>> ")
#    return bn

def list_objects(bn):
    bucket = conn.get_bucket(bn)
    for key in bucket.list():
        print ("{name}\t{size}\t{modified}".format(
                name = key.name,
                size = key.size,
                modified = key.last_modified,
                ))

def create_object(bn, object_name, object_content):
    bucket = conn.get_bucket(bn)
    key = bucket.new_key(object_name)
    key.set_contents_from_string(object_content)

def delete_object(bn,o):
    bucket = conn.get_bucket(bn)
    for key in bucket.list():
        if key.name == o:
            key.delete()

def uploader(bn,path):
    #Get file info
    b = conn.get_bucket(bn)
    source_path = path
    print("Uploading File "+source_path+" to bucket "+bn)
    source_size = os.stat(source_path).st_size
    # Create a multipart upload request
    mp = b.initiate_multipart_upload(os.path.basename(source_path))
    # Use a chunk size of 50 MiB
    chunk_size = 52428800
    chunk_count = int(math.ceil(source_size / float(chunk_size)))
    # Send the file parts, using FileChunkIO to create a file-like object
    # that points to a certain byte range within the original file. We
    # set bytes to never exceed the original file size.
    for i in range(chunk_count):
        offset = chunk_size * i
        bytes = min(chunk_size, source_size - offset)
        with FileChunkIO(source_path, 'r', offset=offset,
                         bytes=bytes) as fp:
            mp.upload_part_from_file(fp, part_num=i + 1)
    mp.complete_upload()

def downloader(bn,on,path):
   
    b = conn.get_bucket(bn)
    print("Downloading Object "+on+" to Directory "+path+on)
    key = b.get_key(on)
    key.get_contents_to_filename(path+on)
    
def switch_bucket(x):
    y=x.split()
    if len(x.split())>1:
        if y[0] == 'rm':
            delete(y[1])
        elif y[0] == 'c':
            create(y[1])
        elif y[0] == 'mo':
            create_object(y[1],y[2],y[3])
        elif y[0]=='lo':
            list_objects(y[1])
        elif y[0]=='do':
            delete_object(y[1],y[2])
        elif y[0]=='u':
            uploader(y[1],y[2])
        elif y[0]=='d':
            downloader(y[1],y[2],y[3])
    else:
        #print("is not a typo press h to get information")
        if x == 'e':
            return 1
        elif x == 'h':
            h()
        elif x == 'l':
            lists()
        elif x == 'space':
            for i in range(50):
                print()
        
def h():
    print("\n Bucket Functions:")
    print(" - l, list your buckets")
    print(" - rm, delete a bucket")
    print(" - c, create a bucket")
    print("\n Object Functions:")
   # print("\n If you want to use \n this functions you have to \n be in a Bucket \n")
    print(" - lo, list objects")
    print(" - mo, make an object")
    print(" - do, delete an object")
    print(" - u, upload to bucket")
    print(" - d, download from bucket")
    print("\n Others:")
    print(" - h, help")
    print(" - space, make some space")
    print(" - e, exit")