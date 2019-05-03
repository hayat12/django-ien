from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, ListAPIView
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    EventsSerializer,
    UserCreateSerializer,
    CreateEventSerializer,
    CreateConnectionSerializer,
    UploadImageSerializer,
    AdgendaSerializer,
)

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework import permissions

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import UserProfile, Event, Adgenda, Connection, AdgendaInvites
import logging
from rest_framework.permissions import IsAuthenticated
from myapp import helper
import json
import os
import base64
from django.core.files.base import ContentFile
# Create your views here.
logger = logging.getLogger(__name__)
# from rest_framework.permissions import IsAuthenticated


class UserList(ListAPIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = User.objects.all()
    serializer_class = UserSerializer


class ImageBase64(APIView):
    permission_classes = (AllowAny,)
    rep = None

    def get(self, req):
        try:
            img_url = 'myapp/media/logo.png'
            _format, _img_str = img_url.split(';base64,')
            _name, ext = _format.split('/')
            rep = Response(ContentFile(base64.b64decode(
                _img_str), name='{}.{}'.format(_name, ext)))
        except Exception as e:
            rep = Response({'error': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return rep


class UserDetail(APIView):
    permission_classes = (AllowAny,)

    def get(self, req):
        res = None
        try:
            serializer = UserSerializer(req.user)
            res = Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return res

    def post(self, req):
        data = req.data
        dic = {
            'username': data['username'],
            'password': data['username']
        }
        print(dic['username'])
        return Response(1)


class CurrentUser(APIView):
    permission_classes = (AllowAny,)

    def get(self, req, id):
        res = None
        qr = Q()
        q = UserProfile.objects
        hasId = False
        try:
            if id not in [None, '']:
                hasId = True
            if hasId:
                qr = Q(user=id)
                q = q.filter(qr)
                ser = UserProfileSerializer(
                    q, many=True, context={'request': req})
                res = Response(ser.data)
            else:
                res = Response(
                    {'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res


class Events(APIView):
    # permission_classes = (AllowAny,)
    def get(self, req, id):
        res = None
        qr = Q()
        event_id = id
        q = Event.objects
        try:
            qr = Q(pk=event_id)
            q = q.filter(qr)
            ser = EventsSerializer(q, many=True, context={'request': req})
            res = Response(ser.data)
        except Exception as e:
            logger.exception(e)
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res

    def post(self, req):
        print(req.user)
        try:
            # serializer = CreateEventSerializer(data=req.data)
            # if serializer.is_valid():
            #     serializer.save()
            #     res = Response({'success': serializer.data}, status=status.HTTP_201_CREATED)
            dic = req.data
            obj = Event(
                event_name=dic['event_name'],
                event_image=dic['event_image'],
                selected_address=dic['selected_address'],
                location=dic['location'],
                category=dic['category'],
                about_event=dic['about_event'],
                start_time=dic['start_time'],
                start_date=dic['start_date'],
                end_time=dic['end_time'],
                end_date=dic['end_date'],
                created_by=req.user,
                user=req.user
            )
            obj.save()
            res = Response({'success': 1}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(e)
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res


class EventList(APIView):
    permission_classes = (AllowAny,)

    def get(self, req):
        res = None
        qr = Q()
        print(req.user)
        serializer = UserSerializer(req.user)
        user_id = serializer.data['id']
        q = Event.objects  # .values_list('id', flat=True).filter(user=d)
        try:
            qr = Q(user=user_id)
            print(user_id)
            q = q.filter(qr)
            ser = EventsSerializer(q, many=True, context={'request': req})
            res = Response(ser.data)
        except Exception as e:
            logger.exception(e)
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res


class CreateUserView(APIView):
    permission_classes = (AllowAny,)
    res = None

    def post(self, req):
        try:
            data = req.data
            user = User.objects.create_user(username=data['email'],
                                            email=data['email'],
                                            password=data['password'])
            res = Response({'success': 1})
        except Exception as e:
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res


class UpdateUser(APIView):
    permission_classes = (AllowAny,)

    def put(self, req):

        try:
            dic = req.data
            usr = User.objects.get(pk=dic['id'])
            usr.first_name = dic['first_name']
            usr.last_name = dic['last_name']
            usr.save()
            obj = UserProfile(
                pk=dic['id'],
                email=dic['email'],
                phone=dic['phone'],
                company_name=dic['company_name'],
                steps=int(1),
                designation=dic['designation'],
                about_me=dic['about_me'],
                address=dic['address'],
                dob=dic['dob'],
                # organization_name=dic['organization_name'],
                position_held=dic['position_held'],
                passport=dic['passport'],
                account_no=dic['account_no'],
                # main_interest=dic['main_interest'],
                # sub_interest=dic['sub_interest'],
                created_date=helper.current_date(),
                user=req.user,
                created_by=req.user)
            obj.save()
            if obj:
                res = Response(1)
            else:
                res = Response(
                    {'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res


class uploadUserProfile(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = UserProfile.objects.all()
    serializer_class = UploadImageSerializer


class SearchList(APIView):
    permission_classes = (AllowAny,)

    def get(self, req):
        res = None
        qr = Q()
        term = req.GET.get('term')
        serializer = UserSerializer(req.user)
        user_id = serializer.data['id']
        q = Event.objects
        try:
            qr = Q(user=user_id)
            q = q.filter(qr)
            if term not in [None, '']:
                qr = Q(event_name__icontains=term)
                q = q.filter(qr)
                hasfilter = True
            else:
                qr = Q(user=user_id)
                q = q.filter(qr)
            ser = EventsSerializer(q, many=True, context={'request': req})
            res = Response(ser.data)

        except Exception as e:
            logger.exception(e)
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_404_NOT_FOUND)
        return res


class getTicket(APIView):
    permission_classes = (AllowAny,)
    res = None
    haseUser = False
    isCreated = False
    qr = Q()

    def get(self, req, id):
        serializer = UserSerializer(req.user)
        user_id = serializer.data['id']
        event_id = id
        try:
            queryset = Event.objects.filter(pk=id)
            for obj in queryset:
                created_by_id = obj.created_by,
                if created_by_id not in [None, '']:
                    isCreated = True
                else:
                    res = Response(
                        {'event': 0, 'message': 'event has been closed'}, status=status.HTTP_404_NOT_FOUND)
            if user_id not in [None, '']:
                haseUser = True
            if id in [None, '']:
                res = Response({'error': 1}, status=status.HTTP_404_NOT_FOUND)
            if haseUser and isCreated:
                dic = {
                    'user': user_id,
                    'cons_id': user_id,
                    'event_id': event_id,
                    'created_by': 1,
                }
                ser = CreateConnectionSerializer(data=dic)
                if ser.is_valid():
                    ser.save()
                    res = Response(
                        {'success': 1}, status=status.HTTP_201_CREATED)
                else:
                    res = Response(
                        {'error': 1}, status=status.HTTP_404_NOT_FOUND)
            else:
                res = Response({'error': 1}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_400_BAD_REQUEST)
        return res


class AdgendaAPI(APIView):
    permission_classes = (AllowAny,)
    res = None

    def get(self, req, id):
        qr = Q()
        q = Adgenda.objects
        try:
            qr = Q(pk=id)
            q = q.filter(qr)
            ser = AdgendaSerializer(q, many=True, context={'request': req})
            res = Response(ser.data)
        except Exception as e:
            res = Response({'error': 1, "message": str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res

    def put(self, req, id):
        try:
            o = Adgenda.objects.get(pk=id)
            data = req.data
            o.title = data['title']
            o.address = data['address']
            o.notes = data['notes']
            o.start_time = data['start_time']
            o.start_date = data['start_date']
            o.user= req.user
            o.save()
            res = Response({'success': 1})
        except Exception as e:
            res = Response({'error': 1, "message": str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res


class CreateAdgena(APIView):
    res = None
    haseUser = False

    def post(self, req):
        try:
            dic = req.data
            obj = Adgenda(
                title=dic['title'],
                address=dic['address'],
                notes=dic['notes'],
                start_time=dic['start_time'],
                start_date=dic['start_date'],
                created_by=req.user,
                user=req.user
            )
            obj.save()
            invites = dic['invites']
            if invites not in (None, ''):
                for invi in invites:
                    invite_obj = AdgendaInvites(
                        user=req.user,
                        invite_id=req.user,
                        status=0,
                        adg_id=req.user,
                        created_by=req.user
                    )
                    invite_obj.save()
                    res = Response(
                        {'success': 1}, status=status.HTTP_201_CREATED)
        except Exception as e:
            res = Response({'error': 1, "message": str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res

    def get(self, req):
        res = None
        qr = Q()
        serializer = UserSerializer(req.user)
        user_id = serializer.data['id']
        q = Adgenda.objects
        try:
            qr = Q(user=user_id)
            q = q.filter(qr)
            ser = AdgendaSerializer(q, many=True, context={'request': req})
            res = Response(ser.data)
        except Exception as e:
            logger.exception(e)
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res


class Connections(APIView):
    permission_classes = (AllowAny,)

    def get(self, req):
        res = None
        qr = Q()
        q = Connection.objects
        try:
            qr = Q(pk=1)
            q = q.filter(qr)
            res = Response(1)
        except Exception as e:
            logger.exception(e)
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res
