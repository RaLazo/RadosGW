# Title: RadosGW - Connector - Class
# Eng.: Rafael Lazenhofer
# Ver.: 2.0
# Date: 12.01.2018
import math, os
import boto
import boto.s3.connection
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

    def public_link(self, object,rights,vality):
        '''
        make a public link to an object
        rights:
        1 . . . . Signlink
        2 . . . . normallink
        vality:
        in sec. Example: 3600s = 60min
        '''
        bucket = self.conn.get_bucket(self.bucketname)
        key = bucket.get_key(object)
        key.set_canned_acl('public-read')
        if rights==1:
            url = key.generate_url(vality, query_auth=True, force_http=True)
        else:
            url = key.generate_url(vality, query_auth=False, force_http=True)
        '''
        file = open("URL.txt","a")
        file.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+"\t"+object+": "+url+"\n")
        file.close()
        '''
    def rights_mangement(self,object,right):
        '''
        Set the rights of an object
        rights:
        1 . . . . private
        2 . . . . public
        '''
        bucket = self.conn.get_bucket(self.bucketname)
        key = bucket.get_key(object)
        if right == 1:
            key.set_canned_acl('private')
        else:
            key.set_canned_acl('public-read') 

    def show_data(self,typ):
        """
        Show data of the class
        OPTIONS:
            1 . . . access_key,secret_key,host
            2 . . . bucketname, downloadpath,bucketstatus
            0 or another value show both compained
        RETURN VALUE:
            [INFORMATION NAME] [INFORMATION]
        """
        if typ == 1:
            var = "Access_key: "+self.access_key +" Secret_key: "+self.secret_key+" Host: "+self.server
        elif typ == 2:
            var = "Bucket: "+self.bucketname+" Downloadpath: "+self.dp+" Bucketstatus: "+str(self.inbucket)
        else:
            var = ("Access_key: "+self.access_key +" Secret_key: "+self.secret_key+" Host: "+self.server+" Bucket: "+self.bucketname+" Downloadpath: "+self.dp+" Bucketstatus: "+str(self.inbucket))

        return var.split()


    def lists(self):
        """
        This function list all avalible buckets of the user
        RETURN VALUE:
            [name of the bucket] [creation date]
        """
        b=[]
        for bucket in self.conn.get_all_buckets():
            b.append("{name} {created}".format(name = bucket.name, created = bucket.creation_date))
        return b

    def create(self):
        '''
        This function create a bucket
        '''
        self.conn.create_bucket(self.bucketname)

    def bn(self,bn):

        """
        Check if the Bucket exist and set the Bucketname of the class
        RETURN VALUE:
           1 . . . . . Bucketname was set
           0 . . . . . ERROR Bucket doesn´t exist
        """
        for bucket in self.conn.get_all_buckets():
            if bucket.name == bn:
                self.bucketname = bn
                i=1
                return 1

        try:
             i
        except NameError:
            return 0

    def delete(self):
        '''
        This function delete a bucket
        (Doesn´t  if it`s full or empty)
        '''
        bucketname = self.conn.get_bucket(self.bucketname)
        for key in bucketname:
            key.delete()
        self.conn.delete_bucket(bucketname)

    def list_objects(self):
        '''
        Lists the objects of an bucket
        RETURN VALUE:
            [object_name] [object_size] [modification_date]
        '''
        b=[]
        bucket = self.conn.get_bucket(self.bucketname)
        for key in bucket.list():
            if(len(str(key.get_acl()))== 42):
                rigth = "Privat"
            else:
                rigth="Public"
            b.append("{name} {size} {modified} {acl}".format(
                    name = key.name,
                    size = key.size,
                    modified = key.last_modified,
                    acl = rigth,
                    ))
        return b

    def create_object(self, object_name, object_content):
        '''
        Create an object in a bucket
        '''
        bucket = self.conn.get_bucket(self.bucketname)
        key = bucket.new_key(object_name)
        key.set_contents_from_string(object_content)

    def downloader(self,object_name):
        '''
        Downloads an object from an bucket
        '''
        b = self.conn.get_bucket(self.bucketname)
        #print("Downloading Object "+object_name+" to Directory "+"\\"+self.dp+object_name)
        key = b.get_key(object_name)
        key.get_contents_to_filename(self.dp+"\\"+object_name)

    def uploader(self,path):
        '''
        Upload files to a bucket
        (this function use FileChunkIO)
        '''
        b = self.conn.get_bucket(self.bucketname)
        source_path = path

        try:    
            source_size = os.stat(source_path).st_size
        except FileNotFoundError:
            print("ERROR: File not Found")
            return
        size_of_file = os.path.getsize(source_path)
        if(size_of_file>1000000000):
            #print("FileChunkIO:\nChunk_size: "+str(chunk_size)+"\nChunks: "+str(chunk_count)+"\nUploading File "+source_path+" to bucket "+self.bucketname)
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
            #print("Uploading File "+source_path+" to bucket "+self.bucketname)
            k = Key(b)
            paths=path.split("/")
            k.key = paths[len(paths)-1] 
            k.set_contents_from_filename(path)

    def delete_object(self,o):
        '''
        This function delete an object of an bucket
        '''
        bucket = self.conn.get_bucket(self.bucketname)
        for key in bucket.list():
            if key.name == o:
                key.delete()