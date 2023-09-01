import swapper 

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response    
from rest_framework.viewsets import ModelViewSet

from comments.views import CommentViewSet
from helpcentre.serializers.faq_serializer import *
from helpcentre.models.faq import *
from kernel.utils.rights import has_helpcentre_rights
from kernel.managers.get_role import get_role
from notifications.actions import push_notification
from helpcentre.utils import get_base_category

Person=swapper.load_model('kernel','Person')
Maintainer=swapper.load_model('kernel','Maintainer')

class FaqView(ModelViewSet):
    queryset=Faq.objects.all()
    serializer_class=FaqSerializer
    http_method_name=[
        'get',
        'post',
        'patch',
        'delete',
        'options',
        'head',
    ]
    permission_classes=[IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        request_keys=request.data.keys()
        if not has_helpcentre_rights(request.user):
            if 'query' in request_keys or 'answer' in request_keys or 'answer_file' in request_keys:
                return Response(
                    data={
                        'Error':'You cannot perform this action'
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
            