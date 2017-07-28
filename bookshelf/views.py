import requests
import json
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import MyShelf, FcmToken, MyBooks
from django.forms.models import model_to_dict
from .key import google_api
from rest_framework import routers, serializers, viewsets

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

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def api_saveToken(request):
    tokenType = int(request.GET.get("type"))
    fcmToken = FcmToken.objects.filter(tokenType=tokenType, shelf__user=request.user)
    if len(fcmToken) == 0:
        fcmToken = FcmToken()
        fcmToken.shelf = MyShelf.objects.get(user=request.user)
        fcmToken.token = request.GET.get("token")
        fcmToken.tokenType = tokenType
        fcmToken.save()
        return Response(model_to_dict(fcmToken))
    else:
        fcmToken = fcmToken[0]
        fcmToken.token = request.GET.get("token")
        fcmToken.save()
        return Response(model_to_dict(fcmToken))

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def api_saveTotalLength(request):
    mySelfs = MyShelf.objects.filter(user=request.user)
    mySelfs.totalShelfLen = request.GET.get('len')
    mySelfs.save()
    return Response(model_to_dict(mySelfs))

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def api_getBookshelf(request):
    mySelfs = MyShelf.objects.get(user=request.user)
    return Response(model_to_dict(mySelfs))

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def api_sendMsg(request):
    send_type = int(request.GET.get('type'))

    fcmToken = FcmToken.objects.get(shelf__user=request.user, tokenType=send_type)
    request_url = "https://fcm.googleapis.com/fcm/send"

    # 헤더 설정
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key='+google_api,
    }

    print(headers)
    # camera app으로 보냄
    if send_type == 0:
        length = request.GET.get('length')
        payload = {}
        datas = {}
        notification = {}

        datas['pos'] = length
        datas['title'] = 'Smart Bookshelf'
        datas['msg'] = 'position information'
        # 페이로드 설정
        payload['to'] = fcmToken.token
        payload['data'] = datas


        print(payload)


        # 응답 객체
        response = requests.post(request_url, data=json.dumps(payload, separators=(',', ':'), sort_keys=True).encode('utf8'), headers=headers)

        print(response.content)
        print(response.status_code)
        return Response(response.json())

    else:
        keyword = request.GET.get('keyword')
        position = request.GET.get('pos')
        totalLength = request.GET.get('totlen')

        # 페이로드 설정
        payload = {
            'to': fcmToken.token,
            'data': {
                'keyword': keyword,
                'position': position,
                'totallen': totalLength,
                'type': send_type,
                'title': 'Smart Bookshelf',
                'msg': 'Detected a book',
            }
        }

        print(payload)

        # 응답 객체
        response = requests.post(request_url, data=json.dumps(payload, separators=(',', ':'), sort_keys=True).encode('utf8'), headers=headers)

        print(response.content)
        print(response.status_code)
        return Response(response.json())

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyBooks
        fields = ('shelf', 'bookTitle', 'bookImgUri', 'bookPublisher', 'bookDesc', 'bookInfo', 'booksPosLen', 'readPos', 'remark',)

class BooksViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BooksSerializer

    def get_queryset(self):
        user = self.request.user
        print(user)
        return MyBooks.objects.filter(shelf__user=user)

