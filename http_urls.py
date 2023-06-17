from django.urls import path, include
from rest_framework import routers

from helpcentre.views import (
    QueryViewSet,
    HelpcentreCommentViewset,
    faq_view,
    quickguide_view

)
from helpcentre.views.allows_polyjuice import AllowsPolyjuiceView

app_name = 'helpcentre'

router = routers.SimpleRouter()
router.register(r'query', QueryViewSet, basename='query')
router.register(r'comments', HelpcentreCommentViewset, basename='comment')
router.register(r'faqs', faq_view, basename='faq')
router.register(r'quickguide', quickguide_view, basename='quickguide')

urlpatterns = [
    path('', include(router.urls)),
    path('allows_polyjuice/', AllowsPolyjuiceView.as_view()),
]
