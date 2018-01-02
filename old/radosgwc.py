
# Title: RadosGW - Connector
# Eng.: Rafael Lazenhofer
# Ver.: 1.0
# Date: 21.12.2017
import boto
import boto.s3.connection
import functions as func


# main
print("RadosGW - Connector")
i=0
j=0    
while i != 1:
    x=input(">>> ")
    i=func.switch_bucket(x)

