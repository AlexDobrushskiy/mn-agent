from django.urls import re_path

from main.views import MasternodeApiView, RegticketApiView, ChunkApiView, MNConnectionApiView, MasternodeUIApiView
from rest_framework.authtoken import views

urlpatterns = [
    re_path(r'token-auth/', views.obtain_auth_token),

    re_path(r'^ui/masternode/?$', MasternodeUIApiView.as_view()),

    re_path(r'^masternode/?$', MasternodeApiView.as_view()),
    re_path(r'^regticket/?$', RegticketApiView.as_view()),
    re_path(r'^chunk/?$', ChunkApiView.as_view()),
    re_path(r'^mn_connection/?$', MNConnectionApiView.as_view()),
]
