from django.urls import re_path

from main.views import MasternodeApiView

urlpatterns = [
    re_path(r'^masternode/?$', MasternodeApiView.as_view()),
    # re_path(r'^regticket/?$', RegticketApiView.as_view()),
]
