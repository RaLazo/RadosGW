
# Title: RadosGW - Connector
# Eng.: Rafael Lazenhofer
# Ver.: 1.0
# Date: 21.12.2017
from rgwclass import rgw


# main
print("RadosGW - Connector")
i=0
j=0    
r=rgw('C8QE7PRORJGH4B52ZOZ7','VfuN9KgJaFfkL0POJbkVJ8FnpzaRgTHzowfj3Xy3','172.16.136.3')
while i != 1:
    x=input(">>> ")
    i=r.switch(x)