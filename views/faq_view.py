from helpcentre.models import Faq
from helpcentre.serializers.faq_serializer import FaqSerializer

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response


class FaqViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    # permission_classes = [IsTeamMemberOrReadOnly]
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
        'options',
        'head',
    ]

    # def perform_create(self, serializer):
    #     serializer.save(creator=self.request.user)
