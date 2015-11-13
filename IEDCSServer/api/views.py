from django.shortcuts import render
from rest_framework import generics
from core.models import User, Player, Device, Content, Purchase
from core.serializers import *
from httplib import HTTPResponse
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import json


class UserLogin(generics.ListCreateAPIView):
    """<b>User Login</b>"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    allowed_methods = ['get']

    def get(self, request):
        """
        Gets user id if credentials are correct




        <b>Details</b>

        METHODS : GET



        <b>RETURNS:</b>

        - 200 OK.

        - 400 BAD REQUEST

        - 401 UNAUTHORIZED

        username -- registration username
        password -- registration password
        ---
        omit_parameters:
        - form
        """
        if 'password' in request.GET and 'username' in request.GET:
            try:
                user = User.objects.get(username__iexact = request.GET.get('username'))
                # if user.check_password(request.GET.get('password')):
                passwd = request.GET.get('password')
                if passwd == user.password:
                    return Response(status=status.HTTP_200_OK, data={'id': user.userID, 'first_name': user.firstName,
                                                                     'last_name': user.lastName, 'email': user.email})
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
                # print e
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ContentByUser(generics.ListCreateAPIView):
    """<b>Content by User</b>"""
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    allowed_methods = ['get']

    def get(self, request, pk=None):
        """
        Gets purchased content by given user id




        <b>Details</b>

        METHODS : GET



        <b>RETURNS:</b>

        - 200 OK.

        ---
        omit_parameters:
        - form
        """
        try:
            int_id = int(pk)
            user = User.objects.get(userID=int_id)
            purchases = Purchase.objects.all().filter(user=user)
            resp = []
            for p in purchases:
                resp += [p.content]
            self.queryset = resp
        except:
            self.queryset = []
        return self.list(request)


class UserDevice(generics.ListCreateAPIView):
    """<b>Gets User device hash and key</b>"""
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    allowed_methods = ['get']

    def get(self, request, pk=None, hash=None):
        """
        Gets device hash and key by given User




        <b>Details</b>

        METHODS : GET



        <b>RETURNS:</b>

        - 200 OK.

        - 204 NO CONTENT

        ---
        omit_parameters:
        - form
        """
        try:
            int_id = int(pk)
            hash_str = str(hash)
            user = User.objects.get(userID=int_id)
            player = Player.objects.all().filter(userID=user.userID)
            device = Device.objects.all().filter(player=player,deviceHash=hash_str)
            if len(device) == 0:
                self.queryset = []
                return Response(status=status.HTTP_204_NO_CONTENT)
            self.queryset = device
        except Exception as e:
            print e
            return Response(status=status.HTTP_204_NO_CONTENT)
        return self.list(request)
