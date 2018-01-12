# Title: RadosGW - Connector
# Eng.: Rafael Lazenhofer
# Ver.: 1.0
# Date: 21.12.2017
from rgwclass import rgw
# main
print("\nRadosGW - Connector\n")
i=0
j=0
file = open("UserData.txt","r") 
string=file.read()
string=string.split("\n")    
r=rgw(string[0],string[1],string[2])
while i != 1:
    if r.inbucket==0:
        x=input(">>> ")
        i=r.switch(x)
    else:
        x=input(r.bucketname+">>> ")
        i=r.switch(x)
