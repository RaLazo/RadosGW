<p align="center">
  <img src="GUI/icon/Ceph_OSS.png" width=450px height=150px />
</p>

RadosGW - Connector
=================

Dieses Programm baut eine Verbindung zu einem RadosGW eines Ceph - Clusters
auf. Wenn diese Verbindung steht kann man z.B.: Buckets erstellen,auflisten, . . .  

Inhaltsverzeichnis
=================

  * [RadosGW - Connector](#radosgw-connector)
    * [Erster Schritt](#erster_schritt)
    * [Verwendung](#verwendung)
  * [RadosGW - Connector GUI](#radosgw-connector-gui)
  * [RadosGW - Connector Webinterface](#radosgw-connector-webinterface)

Erster_Schritt
=================
Zuerst muss man die boto & FileChunkIO libary für python heruntergeladen werden.
(Falls man python3 noch nicht installiert ist bitte nachholen!!!). 

```
pip install boto
pip install FileChunkIO
```
Verwendung
=================

Die Datei radosgwc.py muss mit dem Pythoninterpreter ausgeführt werden: 

```
pyhton radosgwc.py
```
Alle Option erhält man mit 'h' => help
```
RadosGW - Connector
>>> h

 Bucket Functions:
 - l, list your buckets
 - rm, delete a bucket
 - c, create a bucket

 Object Functions:
 - lo, list objects
 - mo, make an object
 - do, delete an object
 - u, upload to bucket
 - d, download from bucket

 Others:
 - h, help
 - space, make some space
 - e, exit
>>>
```
RadosGW-Connector-GUI
=================

Ist eine Grafischebenutzeroberfläche um Buckets zu verwalten 
Zurzeit ist diese noch in Arbeit und nicht voll funktionsfähig. 

Der derzeitige entwurf sieht wie folgt aus:

<p align="center">
  <img src="GUI/icon/GUI.PNG" />
</p>

RadosGW-Connector-Webinterface
=================

Ist eine Weboberfläche über die man leicht Buckets verwalten kann, diese befindet 
sich derzeit auch nochh in Arbeit