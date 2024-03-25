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

from user.models import User
from user.serializers import UserSerializer


# Create your views here.

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