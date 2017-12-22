#Title: Bucket Creater
#Ing.: Rafael Lazenhofer
#Date: 21.12.2017
#Ver.: 1.0
import boto
import boto.s3.connection
print("Bucket Creater:")
bucketname=raw_input("Enter bucket name: ")
# Hier werden die Userdaten eingetragen
access_key = 'C8QE7PRORJGH4B52ZOZ7'
secret_key = 'VfuN9KgJaFfkL0POJbkVJ8FnpzaRgTHzowfj3Xy3'
#Erstellung der Verbindung
conn = boto.connect_s3(
aws_access_key_id = access_key,
aws_secret_access_key = secret_key,
host = 'node1',
is_secure=False,
calling_format = boto.s3.connection.OrdinaryCallingFormat(),
)
# Erstellen des Buckets
bucket = conn.create_bucket(bucketname)
for bucket in conn.get_all_buckets():
        print "{name}\t{created}".format(
                name = bucket.name,
                created = bucket.creation_date,
)




