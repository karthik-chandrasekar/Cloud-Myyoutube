# Create your views here.
import mimetypes
from django.shortcuts import render_to_response
from django import  forms
from django.conf import settings
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.template import RequestContext
from datetime import datetime
from models import AllVidFileUrl
import math


class UploadForm(forms.Form):
    file = forms.FileField(label='Select photo to upload')


class RateForm(forms.Form):
    rate = forms.CharField()

def index(request):
    def store_in_s3(p_obj, content, b):
        file_name = p_obj.name
        mime = mimetypes.guess_type(file_name)[0]
        k = Key(b)
        #import pdb;pdb.set_trace()
        
        k.key = p_obj.id
        k.set_metadata("Content-Type", mime)
        k.set_contents_from_string(content)
        k.set_acl("public-read")
      
    

    def delete(file_id, b):
        k = Key(b)
        k.key = file_id
        b.delete_key(k)
        
            
        
        

    #Creating S3 connection 
    conn = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
    b = conn.create_bucket("rafmyyoutubebucket")

    


    photos = AllVidFileUrl.objects.all().order_by("-rate")
    if not request.method == "POST":
        f = UploadForm()
        return render_to_response("myyoutube/index.html", {"form":f, "photos":photos}, context_instance=RequestContext(request))
    
    f = UploadForm(request.POST, request.FILES)
    
    if f.is_valid():     
        fil = request.FILES["file"]
        file_name = fil.name
        
        p_obj = AllVidFileUrl(url="http://d1nfhxlcn71vv.cloudfront.net/", uploaded=datetime.now(), name=file_name, rate=0, rate_num=0)
        p_obj.save()
        content = fil.read()
        store_in_s3(p_obj, content, b)
   
    elif (request.POST.get('rate', 0) !=0):
        r_temp = request.POST.get('rate', 0)
        
        
        r = r_temp[0]
        file_id = r_temp[1:]
        for file_obj in AllVidFileUrl.objects.all():
            if file_obj.id==int(file_id):
                file_obj.rate_num += 1
                file_obj.rate = math.ceil( ((file_obj.rate + int(r))/ file_obj.rate_num)*100)/100
                file_obj.save()
       
    elif request.POST.get('delete'):
        file_id = request.POST.get('delete')
        delete(file_id, b)
        
        for file_obj in AllVidFileUrl.objects.all():
            if file_obj.id==int(file_id):
                file_obj.delete()
                

        
            
    else:
        return render_to_response("myyoutube/index.html", {"form":f, "photos":photos}, context_instance=RequestContext(request))    

    
    photos = AllVidFileUrl.objects.all().order_by("-rate")
    return render_to_response("myyoutube/index.html", {"form":f, "photos":photos}, context_instance=RequestContext(request))
