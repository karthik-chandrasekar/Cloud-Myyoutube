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

class UploadForm(forms.Form):
    file = forms.FileField(label='Select photo to upload')


class RateForm(forms.Form):
     rate = forms.CharField()

def index(request):
    def store_in_s3(filename, content, b):
        mime = mimetypes.guess_type(filename)[0]
        k = Key(b)
        k.key = filename
        k.set_metadata("Content-Type", mime)
        k.set_contents_from_string(content)
        k.set_acl("public-read")
      
    def display(b):
        all_files_url_list = []
        k = Key(b)
        for ele in k.bucket.get_all_keys():
            file_name = ele.name
            file_url = "http://s3.amazonaws.com/rafmyyoutubebucket/"+file_name
            all_files_url_list.append(file_url)
        return all_files_url_list
        

    #Creating S3 connection 
    conn = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
    b = conn.create_bucket("rafmyyoutubebucket")
    all_files_url_list = display(b)

    photos = AllVidFileUrl.objects.all()#.order_by("uploaded")
    if not request.method == "POST":
        f = UploadForm()
        return render_to_response("myyoutube/index.html", {"form":f, "photos":photos, "files_url_list":all_files_url_list}, context_instance=RequestContext(request))
    
    f = UploadForm(request.POST, request.FILES)
    if ((not f.is_valid()) and (request.POST.get('rate', 0) == 0)):
        return render_to_response("myyoutube/index.html", {"form":f, "photos":photos, "files_url_list":all_files_url_list}, context_instance=RequestContext(request))
    if f.is_valid():     
        file = request.FILES["file"]
        filename = file.name
        content = file.read()
        store_in_s3(filename, content, b)
        p_obj = AllVidFileUrl(url="http://s3.amazonaws.com/rafmyyoutubebucket/" + filename, uploaded=datetime.now(), name=filename, rate=0, rate_num=0)
        p_obj.save()
   
    elif (request.POST.get('rate', 0) !=0):
        r = request.POST.get('rate', 0)
        photos = AllVidFileUrl.objects.all()#.order_by("-uploaded")
        for file_obj in photos:
            file_obj.rate_num += 1
            file_obj.rate = (file_obj.rate + int(r)) / file_obj.rate_num
            file_obj.save() 
        photos = AllVidFileUrl.objects.all()#.order_by("-uploaded")
        
    return render_to_response("myyoutube/index.html", {"form":f, "photos":photos, "files_url_list":all_files_url_list}, context_instance=RequestContext(request))
