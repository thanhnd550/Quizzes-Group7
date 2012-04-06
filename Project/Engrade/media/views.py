# Create your views here.
from media.models import Media
from django.shortcuts import HttpResponse,render_to_response
from django.core.files.base import ContentFile

def post(request):
    image=request.POST.get('file')
    p1=Media(id=1)
    p1.save()
    if image:
        p=Media.objects.get(id=1)
        file_content= ContentFile(image)
        p.image.save(image,file_content)


    return render_to_response('media.html',{'show':p1.image})