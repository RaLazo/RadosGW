# Title: RadosGW - Connector - Class
# Eng.: Rafael Lazenhofer
# Ver.: 1.0
# Date: 28.12.2017
import math, os
import boto
import boto.s3.connection
from boto.s3.key import Key
from filechunkio import FileChunkIO

class rgw(object):
    #access_key = 'C8QE7PRORJGH4B52ZOZ7'
    #secret_key = 'VfuN9KgJaFfkL0POJbkVJ8FnpzaRgTHzowfj3Xy3'
    #server = '172.16.136.3'
    def __init__ (self, access_key,secret_key, server):
        self.access_key = access_key
        self.secret_key = secret_key
        self.server = server
        self.conn = boto.connect_s3(
        aws_access_key_id = self.access_key,
        aws_secret_access_key = self.secret_key,
        host = self.server,
        is_secure=False,
        calling_format = boto.s3.connection.OrdinaryCallingFormat(),
        )
        self.bucketname = 'empty'
        self.dp = 'empty'
    
    def show_data(self):
        print("Access_key: "+self.access_key)
        print("Secret_key: "+self.secret_key)
        print("Host: "+self.server)
        print("Bucket: "+self.bucketname)
        print("Downloadpath: "+self.dp)

    def __lists(self):
        for bucket in self.conn.get_all_buckets():
            print ("{name}\t{created}".format(
                name = bucket.name,
                created = bucket.creation_date,
            )) 

    def download_path(self,path):
        self.dp = path

    def __create(self):
        self.conn.create_bucket(self.bucketname)
    
    def bn(self,bn):
        self.bucketname = bn

    def __delete(self):
        bucketname = self.conn.get_bucket(self.bucketname)
        for key in bucketname:
            key.delete()
        self.conn.delete_bucket(bucketname)
    
    def __list_objects(self):
        bucket = self.conn.get_bucket(self.bucketname)
        for key in bucket.list():
            print ("{name}\t{size}\t{modified}".format(
                    name = key.name,
                    size = key.size,
                    modified = key.last_modified,
                    ))

    def __create_object(self, object_name, object_content):
        bucket = self.conn.get_bucket(self.bucketname)
        key = bucket.new_key(object_name)
        key.set_contents_from_string(object_content)

    def __downloader(self,object_name):
        b = self.conn.get_bucket(self.bucketname)
        print("Downloading Object "+object_name+" to Directory "+self.dp+object_name)
        key = b.get_key(object_name)
        key.get_contents_to_filename(self.dp+object_name)

    def __uploader(self,path):
        #Get file info
        b = self.conn.get_bucket(self.bucketname)
        source_path = path
        print("Uploading File "+source_path+" to bucket "+self.bucketname)
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

    def __delete_object(self,o):
        bucket = self.conn.get_bucket(self.bucketname)
        for key in bucket.list():
            if key.name == o:
                key.delete()

    def switch(self,x):
        y=x.split()
        if len(x.split())>1:
            if y[0] == 'mo':
                self.create_object(y[1],y[2],y[3])
            elif y[0]=='lo':
                self.list_objects(y[1])
            elif y[0]=='do':
                self.delete_object(y[1],y[2])
            elif y[0]=='u':
                self.uploader(y[1],y[2])
            elif y[0]=='d':
                self.downloader(y[1],y[2],y[3])
        else:
            #print("is not a typo press h to get information")
            if x == 'e':
                return 1
            elif x == 'rm':
                self.delete()
            elif x == 'c':
                self.create()
            elif x == 'h':
                self.h()
            elif x == 'l':
                self.lists()
            elif x == 'space':
                for i in range(50):
                    print()
    
    def h(self):
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

