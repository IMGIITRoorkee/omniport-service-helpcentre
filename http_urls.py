from django.urls import path, include
from rest_framework import routers

from helpcentre.views.views import (
    QueryViewSet,
    HelpcentreCommentViewset,
)
from helpcentre.views.allows_polyjuice import AllowsPolyjuiceView

app_name = 'helpcentre'

router = routers.SimpleRouter()
router.register(r'query', QueryViewSet, base_name='query')
router.register(r'comments', HelpcentreCommentViewset, base_name='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('allows_polyjuice/', AllowsPolyjuiceView.as_view()),
]
