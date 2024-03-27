from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q, Max, F, Sum
from django.http import HttpResponse, JsonResponse

# Password Hashing and Validating Password
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password

from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User, UserAddress
from user.serializers import UserSerializer, UserAddressSerializer


class UserAddressData(ListAPIView):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer

    def get_queryset(self):
        try:
            username = self.request.GET.get("username")
            return UserAddress.objects.filter(user__username__icontains=username)
        except Exception as e:
            return User.objects.none()

@method_decorator(csrf_exempt, name='dispatch')
class UserCRUD(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            username = self.request.GET.get("username")
            return User.objects.get(username=username)
        except Exception as e:
            return User.objects.none()

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            validate_password(password=data['password'], user=User)
            data['password'] = make_password(data['password'])
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse(JSONRenderer().render(serializer.data), content_type='application/json')
            return HttpResponse(JSONRenderer().render(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # print(e)
            return HttpResponse(JSONRenderer().render({"Error": str(e)}), content_type='application/json',
                                status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            data = request.data
            validate_password(password=data['password'], user=User)
            data['password'] = make_password(data['password'])
            user = User.objects.get(**data)
            serializer = UserSerializer(user, data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse(JSONRenderer().render(serializer.data), content_type='application/json')
            return HttpResponse(JSONRenderer().render(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return HttpResponse(JSONRenderer().render({"Error": str(e)}), content_type='application/json',
                                status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        try:
            data = request.data
            if 'password' in data.keys():
                validate_password(password=data['password'], user=User)
                data['password'] = make_password(data['password'])
            user = User.objects.get(**data)
            serializer = UserSerializer(user, data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse(JSONRenderer().render(serializer.data), content_type='application/json')
            return HttpResponse(JSONRenderer().render(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return HttpResponse(JSONRenderer().render({"Error": str(e)}), content_type='application/json',
                                status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            data = request.data
            # data = request
            if data == '' or data == {}:
                raise TypeError("Give the perfect Payload")
            user = User.objects.get(username=data['username'])
            serializer = UserSerializer(user, data={"is_active": False}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse(JSONRenderer().render({"Message": str(data['username']) + " Deleted Successfully"}),
                                    content_type='application/json')
        except Exception as e:
            return HttpResponse(JSONRenderer().render({"Error": str(e)}), content_type='application/json',
                                status=status.HTTP_400_BAD_REQUEST)


class UserAdditional(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            is_active = self.request.GET.get('is_active')
            user = User.objects.all()
            print(user)
            return user
        except:
            return User.objects.none()

