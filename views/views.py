from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from comments.views import CommentViewSet
from helpcentre.serializers.serializers import *
from kernel.utils.rights import has_helpcentre_rights
from kernel.managers.get_role import get_role


class QueryViewSet(ModelViewSet):
    """
    The view for CRUD operations of a query
    """

    serializer_class = QuerySerializer
    permission_classes = [IsAuthenticated, ]
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
        'options',
        'head',
    ]

    def get_serializer_class(self):
        """
        This function decides the serializer class according to the type of
        request
        :return: the serializer class
        """

        if self.action == 'list':
            return QuerySerializer
        elif self.action == 'retrieve':
            return QueryDetailSerializer
        return QuerySerializer

    def get_queryset(self):
        """
        This function overrides the default get_queryset function and displays
        all the queries to Maintainers (who have helpcentre rights). Other
        users are displayed a list of their asked queries.
        :return: the corresponding queryset to the view accordingly
        """
        
        result = []
        status = ''
        person = self.request.user.person
        if 'status' in self.request.query_params:
            status = self.request.query_params['status']
        if has_helpcentre_rights(self.request.user):
            result = Query.objects.all().order_by('-datetime_modified')
            if status == 'assigned':
                maintainer = get_role(person, 'Maintainer', silent=True)
                return result.filter(assignee=maintainer)
        else:
            result = Query.objects.filter(uploader=person).order_by(
                '-datetime_modified'
            )
        if status == 'opened':
            return result.filter(is_closed=False)
        elif status == 'closed':
            return result.filter(is_closed=True)
        return result

    def partial_update(self, request, *args, **kwargs):
        """
        This function overrides the partial_update function (invoked when PATCH
        request is made). This determines the fields that are not editable by
        normal users which can be edited by Maintainers.
        For example: is_closed and assignee field
        :param request: the request from the client
        :param args: other args
        :param kwargs: other kwargs
        :return: 403 (Forbidden) if the user is not authorized and
        partial_update if user is allowed to perform the same
        """

        request_keys = request.data.keys()
        if not has_helpcentre_rights(request.user):
            if 'assignee' in request_keys or 'is_closed' in request_keys:
                return Response(
                    data={
                        'Error': 'You cannot perform this operation.'
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
        return super(QueryViewSet, self).partial_update(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Overrides the default perform_create and takes in user from the request
        and assigns the person as to the uploader.
        :param serializer:
        """

        person = self.request.user.person
        serializer.save(uploader=person)


class HelpcentreCommentViewset(CommentViewSet):
    """
    The view for CRUD operations of a Helpcentre comment
    """

    http_method_names = [
        'post',
        'options',
        'head',
    ]

    def create(self, request, *args, **kwargs):
        """
        This function overrides the default create function to create a comment
        and then associate it with the given query id.
        :param request: the request from the client
        :param args: args
        :param kwargs: kwargs
        :return: corresponding response and status code
        """

        try:
            query_id = request.data.pop('query_id')
        except AttributeError:
            return Response(
                data={
                    'Error': 'Missing query_id attribute.'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        person = request.user.person
        try:
            query = Query.objects.get(id=query_id)
        except Query.DoesNotExist:
            return Response(
                data={
                    'Error': 'Requested resource does not exist.'
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        if has_helpcentre_rights(request.user) or query.uploader == person:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            comment = serializer.save(commenter=person)
            query.comments.add(comment)
            query.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                data={
                    'Error': 'You cannot perform this operation.'
                },
                status=status.HTTP_403_FORBIDDEN,
            )
