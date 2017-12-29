# RadosGW - Connector


Dieses Programm baut eine Verbindung zu einem RadosGW eines Ceph - Clusters
auf. Wenn diese Verbindung steht kann man z.B.: Buckets erstellen,auflisten, . . .  

## Erster Schritt

Zuerst muss man die boto libary für python herunterladen.
Falls man python2.7 noch nicht installiert hat sollte man die auch tun. 

```
sudo apt-get install python
pip install boto

```
## Verwendung
Die Datei radosgwc.py muss mit dem Pythoninterpreter ausgeführt werden: 

```
pyhton radosgwc.py
```
Alle Option erhält man mit 'h' => help

```
RadosGW - Connector
>>> h
Choose Function
- l, list your buckets
- d, delete a bucket
- c, create a bucket
- lo, list objects of an bucket
- mo. make an object => bucket
- h,help
- e,exit
>>>
```