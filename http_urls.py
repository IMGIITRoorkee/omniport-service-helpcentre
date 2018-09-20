from django.conf.urls import url, include
from rest_framework import routers

from helpcentre.views.views import *

router = routers.DefaultRouter()

router.register(r'query', QueryViewSet, base_name='query')
router.register(r'comments', HelpcentreCommentViewset, base_name='comment')

urlpatterns = [
    url(r'^', include(router.urls)),
]