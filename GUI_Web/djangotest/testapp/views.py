#Django Imports
from django.shortcuts import render, HttpResponse
from testapp.models import login
from django import template

#RadosGW Interface Imports
import math, os
import boto
import boto.s3.connection
from boto.s3.key import Key
from filechunkio import FileChunkIO





#Backend Functions
class backend():

    #Ceck Login data + Show Buckets
    def __init__(request):

        #Get Username from Login Textfields
        username = request.POST.get('username')
        #Get Password from Login Textfields
        password = request.POST.get('password')

        #Set Errorvariable to ''
        #request.session['errorpublish'] = ' ';

        create = request.POST.get('create')  #Check if User wants to create a new User

        if create :        #If User wants to create a new User

            return render(request, 'testapp/create.html')   #Load Create User Page

        else:              #If User wants to login
            #Get password from database where username = username from Login textfield
            corpwd = login.objects.values_list('password', flat=True).get(username = username)

            if  password == corpwd: #If password is correct

                global conn


                #Get User Data
                access_key = login.objects.values_list('accesskey', flat=True).get(username = username, password = corpwd)
                secret_key = login.objects.values_list('secretkey', flat=True).get(username = username, password = corpwd)

                #access_key = 'C8QE7PRORJGH4B52ZOZ7'                     #User Acces Key
                #secret_key = 'VfuN9KgJaFfkL0POJbkVJ8FnpzaRgTHzowfj3Xy3' #User Scret Key
                global server                             #Server IP / Domian

                server = '172.16.136.3'

                #Create connection to RadosGW (Ceph-Cluster)
                conn = boto.connect_s3(
                aws_access_key_id = access_key,
                aws_secret_access_key = secret_key,
                host = server,
                is_secure = False,
                calling_format = boto.s3.connection.OrdinaryCallingFormat(),
                )

                bucketname = 'empty'    #Init bucketname variable
                dp = 'empty'            #Init datapath variable
                inbucket = 0

                #Save User Acces Key in a Session
                request.session['access_key'] = access_key
                #Save User Secret Key in a Session
                request.session['secret_key'] = secret_key
                #Save serve domain/IP in a Session
                request.session['server'] = server
                #Save Username in a Session
                request.session['username'] = username
                #Set default style
                request.session['color'] = 'b'
                #return HttpResponse('Geht')
                #return HttpResponse(access_key)
                #Load Content for Startwebsite (Method call)
                return backend.getback(request)

            else:   #If password is incorrect
                #Return error message
                return HttpResponse ("Wrong User, Password or the User does not exist");

    def create (request):

        usernm = request.POST.get('username')
        passwd = request.POST.get('password')

        Instance = login.objects.create(username=usernm, password=passwd, secretkey=secretk, accesskey=accessk)

        return render(request, 'testapp/index.html')


    #Show Buckets
    def getback (request):

        global conn #Load Connection Variable

        username = request.session['username']  #Load current Username
        error = request.session['errorpublish'] #Error message if something went wrong
        color = request.session['color']
        request.session['errorpublish'] = ''   #Set Errorvariable to ''

        b=[]    #Init List-Variable for existing Bucketnames
        d=[]    #Init List-Variable for Information of Buckets
        for bucket in conn.get_all_buckets():   #Runs as often as the number of Buckets
            #Add Bucketname to List
            b.append("{name}".format(name = bucket.name))
            #Add Bucket-Information to List
            d.append("{created}".format(created = bucket.creation_date))
        #Load Startwebsite

        if color == 'b':
            return render(request, 'testapp/content.html',{'b': b, 'd': d, 'user': username, 'error' : error})

        else:
            return render(request, 'testapp_w/content_w.html',{'b': b, 'd': d, 'user': username, 'error' : error})

    #Get Bucket content
    def getcont (request):

        global conn #Load Connection Variable

        #Get Username from Session
        username = request.session['username']

        #Filter Bucketname from String
        istring = request.GET.get('i')
        isplit = istring.split(' ')
        bucketname = isplit[0]

        #Write Bucketname into Session
        request.session['bucketname'] = bucketname
        color = request.session['color']

        c=[]    #Init List-Variable for Bucket Content
        #Get Bucket Content from RadosGW
        bucket = conn.get_bucket(bucketname)
        for key in bucket.list():
            c.append("{name}".format(
                    name = key.name,
                    ))

        #Check if Bucket has Content
        if not c:
            nocontent = "No Data"
        else:
            nocontent = ""
        #Prepare Bucketname for Website
        isplit = bucketname.split('/')
        bucketname = isplit[0]

        #Load Website for showing Bucket Content
        if color == 'b':
            return render(request, 'testapp/bucketcont.html',{'c': c, 'name': bucketname, 'nocontent': nocontent, 'user': username})
        else:
            return render(request, 'testapp_w/bucketcont_w.html',{'c': c, 'name': bucketname, 'nocontent': nocontent, 'user': username})

    #Get Bucket content again
    def getcontag (request):


        global conn

        username = request.session['username']
        bucketname = request.session['bucketname']
        color = request.session['color']

        c=[]
        bucket = conn.get_bucket(bucketname)
        for key in bucket.list():
            c.append("{name}".format(
                    name = key.name,
                    ))

        if not c:
            nocontent = "No Data"
        else:
            nocontent = ""

        isplit = bucketname.split('/')
        bucketname = isplit[0]

        if color == 'b':
            return render(request, 'testapp/bucketcont.html',{'c': c, 'name': bucketname, 'nocontent': nocontent, 'user': username,})
        else:
            return render(request, 'testapp_w/bucketcont_w.html',{'c': c, 'name': bucketname, 'nocontent': nocontent, 'user': username,})

    #delete Bucket
    def deletebucket(request):

        global conn #Load Connection Variable

        #Load Username from curren Session
        username = request.session['username']
        #Load all selectet Buckets from the Website
        bucketlist = request.POST.getlist('bucket')

        #Run till all Buckets deleted
        for bucketname in bucketlist:
            bucketname = conn.get_bucket(bucketname)
            for key in bucketname:  #Run till all Objects deleted
                key.delete()    #Delete Objects
            conn.delete_bucket(bucketname)  #Delete Bucket

        #Return to Startwebsite
        return backend.getcontag(request)

    #Create Bucket Area
    #Show Bucket Create Website
    def createbsite(request):

        username = request.session['username']
        color = request.session['color']

        if color == 'b':
            return render(request, 'testapp/createbucket.html',{'user': username})
        else:
            return render(request, 'testapp_w/createbucket_w.html',{'user': username})

    #Create Bucket
    def createbucket(request):

        global conn #Load Connection Variable

        #Load Username of current User
        username = request.session['username']
        #Load Bucketname from Textfield
        bucketname = request.POST.get('bucketname')

        color = request.session['color']

        #WBucket - Name Rules detection
        error = 0
        i = 0
        for sign in bucketname:
            if sign == " ":
                error = 1

            elif sign.isupper() == True:
                error = 2

            i = i+1

        if color == 'b':
            #Write Errormessage to Website
            if error == 1: #Error Case 1
                errornote = "Your Bucketname must not contain free spaces"
                return render(request, 'testapp/createbucket.html',{'error': errornote, 'user': username})

            elif error == 2:#Error Case 2
                errornote = "Your Bucketname must not contain capital letters"
                return render(request, 'testapp/createbucket.html',{'error': errornote, 'user': username})

            elif i <= 2:#Error Case 3
                errornote = "Your Bucketname must have at least 3 letters"
                return render(request, 'testapp/createbucket.html',{'error': errornote, 'user': username})

            else:
                conn.create_bucket(bucketname)  #Create Bucket

        else:
            #Write Errormessage to Website
            if error == 1: #Error Case 1
                errornote = "Your Bucketname must not contain free spaces"
                return render(request, 'testapp_w/createbucket_w.html',{'error': errornote, 'user': username})

            elif error == 2:#Error Case 2
                errornote = "Your Bucketname must not contain capital letters"
                return render(request, 'testapp_w/createbucket_w.html',{'error': errornote, 'user': username})

            elif i <= 2:#Error Case 3
                errornote = "Your Bucketname must have at least 3 letters"
                return render(request, 'testapp_w/createbucket_w.html',{'error': errornote, 'user': username})

            else:
                conn.create_bucket(bucketname)  #Create Bucket


            return backend.getcontag(request)
    #Create Bucket Area end

    #Create Object Area
    #Show Object Create Website
    def createobjectsite(request):

        username = request.session['username']
        color = request.session['color']

        if color == 'b':
            return render(request, 'testapp/createobject.html',{'user': username})
        else:
            return render(request, 'testapp_w/createobject_w.html',{'user': username})

    #Create Object
    def createobject(request):

        global conn

        username = request.session['username']

        bucketname = request.session['bucketname']
        object_name = request.POST.get('objectname')
        object_content = request.POST.get('objectcontent')

        bucket = conn.get_bucket(bucketname)
        key = bucket.new_key(object_name)
        key.set_contents_from_string(object_content)

        return backend.getcontag(request)
    #Create Object Area end

    #Object option select
    def select (request):

        delete = request.POST.get('delete')
        download = request.POST.get('download')
        upload = request.POST.get('upload')
        publish = request.POST.get('publish')

        if delete:
            return backend.deleteobject(request)

        elif download:
            return backend.downloadsite(request)

        elif upload:
            return backend.uploadsite(request)

        return backend.publishsite(request)




    #Delete Object
    def deleteobject(request):

        global conn

        username = request.session['username']
        bucketname = request.session['bucketname']
        objectlist = request.POST.getlist('object')

        if not objectlist:
            return backend.getcontag(request)

        for object_name in objectlist:
            bucket = conn.get_bucket(bucketname)
            for key in bucket.list():
                if key.name == object_name:
                    key.delete()

        return backend.getcontag(request)


    #Download Object Area
    #Show Download Website
    def downloadsite (request):

        username = request.session['username']
        object_name = request.POST.get('object')
        request.session['objectdownload'] = object_name

        color = request.session['color']

        if color == 'b':
            return render(request, 'testapp/downloadsite.html',{'user': username})
        else:
            return render(request, 'testapp_w/downloadsite_w.html',{'user': username})

    #Download Object
    def download (request):

        global conn

        username = request.session['username']
        bucketname = request.session['bucketname']
        dp = request.POST.get('dp')
        object_name = request.session['objectdownload']


        b = conn.get_bucket(bucketname)
        print("Downloading Object "+object_name+" to Directory "+dp+object_name)
        key = b.get_key(object_name)
        key.get_contents_to_filename(dp+object_name)

        return backend.getcontag(request)
    #Download Object Area end

    #Upload Object Area
    #Show Upload Object Website
    def uploadsite (request):

        username = request.session['username']
        color = request.session['color']

        if color == 'b':
            return render(request, 'testapp/uploadsite.html',{'user': username})
        else:
            return render(request, 'testapp_w/uploadsite_w.html',{'user': username})

    #Upload Object
    def upload (request):

        global conn

        username = request.session['username']
        bucketname = request.session['bucketname']

        path = request.POST.get('dp')

        #Get file info
        b = conn.get_bucket(bucketname)
        source_path = path
        #print("Uploading File "+source_path+" to bucket "+self.bucketname)
        source_size = os.stat(source_path).st_size
        # Create a multipart upload request
        try:
            mp = b.initiate_multipart_upload(os.path.basename(source_path))
        except FileNotFoundError:
            print("ERROR: File not Found")
            return
        # Use a chunk size of 50 MiB
        chunk_size = 52428800
        chunk_count = int(math.ceil(source_size / float(chunk_size)))
        # Send the file parts, using FileChunkIO to create a file-like object
        # that points to a certain byte range within the original file. We
        # set bytes to never exceed the original file size.
        for i in range(chunk_count):
            offset = chunk_size * i
            bytes = min(chunk_size, source_size - offset)
            with FileChunkIO(source_path, 'r', offset=offset,
                         bytes=bytes) as fp:
                mp.upload_part_from_file(fp, part_num=i + 1)
        mp.complete_upload()

        return backend.getcontag(request)
    #Upload Object Area end

    #Publish Object Area
    #Show Publish Object Website
    def publishsite (request):

        username = request.session['username']
        objectlist = request.POST.getlist('object')
        color = request.session['color']

        if not objectlist:
            return backend.getcontag(request)

        object = objectlist[0]
        request.session['objectpublish'] = object

        if color == 'b':
            return render(request, 'testapp/publishsite.html',{'user': username})
        else:
            return render(request, 'testapp_w/publishsite_w.html',{'user': username})

    #Publish Object
    def publish (request):

        global conn
        global server

        username = request.session['username']
        bucketname = request.session['bucketname']

        prior = request.POST.get('priority')
        valitystr = request.POST.get('time')

        if not valitystr:
            error = "Time must be set"
            return render(request, 'testapp/publishsite.html',{'error': error})

        vality = int(valitystr)
        object = request.session['objectpublish']

        bucket = conn.get_bucket(bucketname)
        key = bucket.get_key(object)
        key.set_canned_acl('public-read')

        if(prior == 1):
            url = key.generate_url(vality, query_auth=True, force_http=True)
        else:
            url = key.generate_url(vality, query_auth=False, force_http=True)

        return render(request, 'testapp/published.html',{'user': username, 'objectname' : object, 'bucketname' : bucketname, 'server' : server})



    #Publish Object Error Handling
    def errorpublish (request):

        request.session['errorpublish'] = 'Choose a Bucket and a Object before publishing'

        return backend.getback(request)
    #Publish Object Area end

    #Show User Data
    def profile (request):

        username = request.session['username']
        secretkey = request.session['secret_key']

        accesskey = login.objects.values_list('accesskey', flat=True).get(username = username)
        password = login.objects.values_list('password', flat=True).get(username = username)

        color = request.session['color']

        if color == 'b':
            return render(request, 'testapp/profile.html', {'user' : username, 'secretkey' : secretkey, 'accesskey' : accesskey, 'password' : password})
        else:
            return render(request, 'testapp_w/profile_w.html', {'user' : username, 'secretkey' : secretkey, 'accesskey' : accesskey, 'password' : password})

    def chcolorw (request):

        global conn
        username = request.session['username']
        secretkey = request.session['secret_key']

        accesskey = login.objects.values_list('accesskey', flat=True).get(username = username)
        password = login.objects.values_list('password', flat=True).get(username = username)

        request.session['color'] = 'w';

        return backend.getback(request)

    def chcolorb (request):

        global conn
        username = request.session['username']
        secretkey = request.session['secret_key']

        accesskey = login.objects.values_list('accesskey', flat=True).get(username = username)
        password = login.objects.values_list('password', flat=True).get(username = username)

        request.session['color'] = 'b';

        return backend.getback(request)
