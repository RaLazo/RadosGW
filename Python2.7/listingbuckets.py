
# Title: Bucket lister
# Eng.: Rafael Lazenhofer
# Ver.: 1.0
# Date: 21.12.2017
import boto
import boto.s3.connection
# Zugangsdaten von User:
print("Ihre Buckets:")
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
# Aufrufen der Buckets
for bucket in conn.get_all_buckets():
        print "{name}\t{created}".format(
                name = bucket.name,
                created = bucket.creation_date,
        )









