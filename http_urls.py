from django.urls import path, include
from rest_framework import routers

from helpcentre.views.views import (
    QueryViewSet,
    HelpcentreCommentViewset,
)
from helpcentre.views.allows_polyjuice import AllowsPolyjuiceView
from helpcentre.views.faq_view import faq_view
from helpcentre.views.quickguide_view import quickguide_view

app_name = 'helpcentre'

router = routers.SimpleRouter()
router.register(r'query', QueryViewSet, basename='query')
router.register(r'comments', HelpcentreCommentViewset, basename='comment')
router.register(r'faqs', QueryViewSet, basename='faq')
router.register(r'quickguide', QueryViewSet, basename='quickguide')

urlpatterns = [
    path('', include(router.urls)),
    path('allows_polyjuice/', AllowsPolyjuiceView.as_view()),
]
