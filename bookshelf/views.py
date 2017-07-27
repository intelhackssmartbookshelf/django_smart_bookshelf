import requests

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import MyShelf
from django.forms.models import model_to_dict

from xmljson import parker
from xml.etree.ElementTree import fromstring
from django.shortcuts import get_object_or_404

from django.shortcuts import render


# Create your views here.
@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def api_saveSelf(request):
    mySelfs = MyShelf.objects.filter(user=request.user)
    if len(mySelfs) == 0:
        mySelf = MyShelf()
        mySelf.user = request.user
        mySelf.lat = request.GET.get('lat')
        mySelf.lng = request.GET.get('lng')
        mySelf.save()
        return Response(model_to_dict(mySelf))
    return Response(model_to_dict(mySelfs[0]))
