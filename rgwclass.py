# Title: RadosGW - Connector - Class
# Eng.: Rafael Lazenhofer
# Ver.: 1.0
# Date: 28.12.2017
import os
import math
import boto
import boto.s3.connection
import datetime
import time
from boto.s3.key import Key
from filechunkio import FileChunkIO

class rgw(object):
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
        self.inbucket = 0

    
    def public_link(self, object):
        bucket = self.conn.get_bucket(self.bucketname)
        key = bucket.get_key(object)
        key.set_canned_acl('public-read')
        print("Do you want signed? [Y/N]:")
        x=input()
        if((x=='y')|(x=='Y')):
            url = key.generate_url(3600, query_auth=True, force_http=True)
        else:
            url = key.generate_url(0, query_auth=False, force_http=True)
        file = open("URL.txt","a")
        file.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+"\t"+object+": "+url+"\n")
        file.close()
        print(url)

    def rights_mangement(self,object,right):
        bucket = self.conn.get_bucket(self.bucketname)
        key = bucket.get_key(object)
        if(right=="pr"):
            key.set_canned_acl('private')
        else:
            key.set_canned_acl('public-read')
        print("completed")

    def showl(self):
        file = open("URL.txt","r") 
        string=file.read()
        file.close()
        print(string)

    def show_data(self):
        print("Access_key: "+self.access_key)
        print("Secret_key: "+self.secret_key)
        print("Host: "+self.server)
        print("Bucket: "+self.bucketname)
        print("Downloadpath: "+self.dp)
        print("Bucketstatus: "+str(self.inbucket))


    def __lists(self):
        for bucket in self.conn.get_all_buckets():
            print ("{name}\t{created}".format(
                name = bucket.name,
                created = bucket.creation_date,
            )) 

        

    def __create(self):
        self.conn.create_bucket(self.bucketname)
        print("completed")

    def bn(self,bn,x):
        if x==1:      
            for bucket in self.conn.get_all_buckets():
                if bucket.name == bn:
                    self.bucketname = bn
                    self.inbucket=1
                    i=1
        else:
            for bucket in self.conn.get_all_buckets():
                if bucket.name == bn:
                    self.bucketname = bn
                    i=1
        try:
             i
        except NameError:
            print ("ERROR: Bucket not exist!")

    def __delete(self):
        bucket = self.conn.get_bucket(self.bucketname)
        for bucket in self.conn.get_all_buckets():
                if bucket.name == self.bucketname:
                    for key in bucket:
                        key.delete()
                    self.conn.delete_bucket(bucket)
                    return
        print("completed")
    
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
        print("completed")

    def __downloader(self,object_name):
        b = self.conn.get_bucket(self.bucketname)
        print("Downloading Object "+object_name+" to Directory "+self.dp+object_name)
        key = b.get_key(object_name)
        key.get_contents_to_filename(self.dp+object_name)

    def __uploader(self,path):
        #Get file info
        
        b = self.conn.get_bucket(self.bucketname)
        source_path = path
        
        try:    
            source_size = os.stat(source_path).st_size
        except FileNotFoundError:
            print("ERROR: File not Found")
            return
        size_of_file = os.path.getsize(source_path)
        if(size_of_file>1000000000):
            print("FileChunkIO:\nChunk_size: "+str(chunk_size)+"\nChunks: "+str(chunk_count)+"\nUploading File "+source_path+" to bucket "+self.bucketname)
            # Create a multipart upload request
            mp = b.initiate_multipart_upload(os.path.basename(source_path))
            # Use a chunk size of 50 MiB
            chunk_size = 52428800
            chunk_count = int(math.ceil(source_size / float(chunk_size)))
            # Send the file parts, using FileChunkIO to create a file-like object
            # that points to a certain byte range within the original file. We
            # set bytes to never exceed the original file size.
            for i in range(chunk_count):
                print(str(chunk_count))
                offset = chunk_size * i
                bytes = min(chunk_size, source_size - offset)
                with FileChunkIO(source_path, 'r', offset=offset,
                                 bytes=bytes) as fp:
                    mp.upload_part_from_file(fp, part_num=i + 1)
            mp.complete_upload()
        else:
            print("Uploading File "+source_path+" to bucket "+self.bucketname)
            k = Key(b)
            paths=path.split("\\")
            k.key = paths[len(paths)-1] 
            k.set_contents_from_filename(path)

    def __delete_object(self,o):
        bucket = self.conn.get_bucket(self.bucketname)
        for key in bucket.list():
            if key.name == o:
                key.delete()
        print("completed")

    def switch(self,x):
        y=x.split()
        if len(x.split())>1:
            
            if (y[0]=='cd') or (self.inbucket==1):
                if(y[0]=='cd'):
                    self.bn(y[1],1) 
            else:
                self.bucketname = y[1]       
            if(self.inbucket==1):
                
                if y[0] == 'mo':
                    try:
                        self.__create_object(y[1],y[2])
                    except IndexError:
                        print("mo [object_name] [content]")
                
                elif y[0]=='do':
                    self.__delete_object(y[1])
                
                elif y[0]=='u':
                    self.__uploader(y[1])
                
                elif y[0]=='pl':
                    self.public_link(y[1])
                elif y[0]=='rights':
                    try:
                        self.rights_mangement(y[1],y[2])
                    except IndexError:
                         print("rights [object_name] [rigth]\n pu for public-read\n pr for private")
                elif y[0]=='d':
                    
                    if self.dp == "empty":
                        try:
                            self.dp=y[2]
                        except IndexError:
                            print("ERROR: Invalid Downloadpath")
                    else:
                        print("insert downpath")
                    self.__downloader(y[1])

            if y[0] == 'downpath':
                self.dp=y[1]
            elif y[0] == 'rm':
                self.__delete()
            elif y[0] == 'c':
                self.__create()
            elif y[0] == 'bn':
                self.bn(y[1],0)
                
            
        else:
            #print("is not a typo press h to get information")
            if x == 'e':
                return 1
            elif x == 'h':
                self.h()
            elif x == 'l':  
                self.__lists()
            elif x == 'space':
                for i in range(50):
                    print()
            elif x =='eb':
                self.inbucket = 0
                self.bucketname = "empty"
            elif x =='showd':
                self.show_data()
            elif x =='showl':
                self.showl()
            elif x =='lo':
                if(self.inbucket==1):
                    self.__list_objects()
            

    def h(self):
        print("\n Bucket Functions:")
        print(" - l, list your buckets")
        print(" - rm, delete a bucket")
        print(" - c, create a bucket")
        print(" - cd, get into a bucket")
        print(" - bn, set a fix bucket name")
        print("\n Object Functions:")
        print("(This Functions can only be used if you are in a bucket!)")
        print(" - lo, list objects")
        print(" - mo, make an object")
        print(" - do, delete an object")
        print(" - u, upload to bucket")
        print(" - d, download from bucket")
        print(" - eb, get out of a bucket")
        print(" - pl, make a publiclink")
        print(" -rights, set the rights for a object")
        print("\n Others:")
        print(" - h, help")
        print(" - space, make some space")
        print(" - showd, shows data of the user")
        print(" - showl, shows your link logfile")
        print(" - downpath, set Downloadpath")
        print(" - e, exit")
        

