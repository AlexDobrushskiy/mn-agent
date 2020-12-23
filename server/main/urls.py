from django.urls import re_path

from main.views import MasternodeApiView, RegticketApiView, ChunkApiView

urlpatterns = [
    re_path(r'^masternode/?$', MasternodeApiView.as_view()),
    re_path(r'^regticket/?$', RegticketApiView.as_view()),
    re_path(r'^chunk/?$', ChunkApiView.as_view()),
]
