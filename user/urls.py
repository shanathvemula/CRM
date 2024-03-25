from django.urls import path
from user.views import UserCRUD

urlpatterns = [
    path('user/', UserCRUD.as_view())
]