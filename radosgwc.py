
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
while i != 1:
    x=raw_input(">>> ")
    i=func.switch(x)

