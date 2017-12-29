# Title: RadosGW - Connector - Class
# Eng.: Rafael Lazenhofer
# Ver.: 1.0
# Date: 28.12.2017
import boto
import boto.s3.connection

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
    
    def show_data(self):
        print("Access_key: "+self.access_key)
        print("Secret_key: "+self.secret_key)
        print("Host: "+self.server)
    
    def lists(self):
        for bucket in self.conn.get_all_buckets():
            print ("{name}\t{created}".format(
                name = bucket.name,
                created = bucket.creation_date,
            )) 
    def bucketname(self, bucketname):
        self.bucketname = bucketname

    def create(self):
        self.conn.create_bucket(self.bucketname)
    
    def delete(self):
        bucketname = conn.get_bucket(self.bucketname)
        for key in bucketname:
            key.delete()
        conn.delete_bucket(bucketname)
    
    def list_objects(self):
        bucket = self.conn.get_bucket(self.bucketname)
        for key in bucket.list():
            print ("{name}\t{size}\t{modified}".format(
                    name = key.name,
                    size = key.size,
                    modified = key.last_modified,
                    ))

    def create_object(self, object_name, object_content):
        bucket = self.conn.get_bucket(self.bucketname)
        key = bucket.new_key(object_name)
        key.set_contents_from_string(object_content)

reinhard=rgw('C8QE7PRORJGH4B52ZOZ7','VfuN9KgJaFfkL0POJbkVJ8FnpzaRgTHzowfj3Xy3','172.16.136.3')
reinhard.show_data()
reinhard.lists()
reinhard.bucketname('hallo')
reinhard.create_object('hallo-3.txt','Hallo Welt!')
reinhard.list_objects()