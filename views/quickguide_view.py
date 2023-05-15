import swapper 

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response    
from rest_framework.viewsets import ModelViewSet

from comments.views import CommentViewSet
from helpcentre.serializers.quickguide_serializer import *
from kernel.utils.rights import has_helpcentre_rights
from kernel.managers.get_role import get_role
from notifications.actions import push_notification
from helpcentre.utils import get_base_category

Person=swapper.load_model('kernel','Person')
Maintainer=swapper.load_model('kernel','Maintainer')

class quickguide_view(ModelViewSet):
    queryset=quickguide.objects.all()
    serializer_class=quickguide_serializer
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
            if 'title' in request_keys or 'description' in request_keys or 'description_file' in request_keys:
                return Response(
                    data={
                        'Error':'You cannot perform this action'
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )