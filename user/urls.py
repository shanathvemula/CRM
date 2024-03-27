from django.urls import path
from user.views import UserCRUD, UserAdditional, UserAddressData

urlpatterns = [
    path('user/', UserCRUD.as_view()),
    path('UserAdditional/', UserAdditional.as_view()),
    path('UserAddressData/', UserAddressData.as_view())
]