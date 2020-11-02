import swapper
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from comments.views import CommentViewSet

from kernel.utils.rights import has_helpcentre_rights
from kernel.managers.get_role import get_role
from notifications.actions import push_notification
from helpcentre.serializers.serializers import *
from helpcentre.utils import get_base_category


Person = swapper.load_model('kernel', 'Person')
Maintainer = swapper.load_model('kernel', 'Maintainer')


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
                return result.filter(assignees=maintainer)
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
        For example: is_closed and assignees field
        :param request: the request from the client
        :param args: other args
        :param kwargs: other kwargs
        :return: 403 (Forbidden) if the user is not authorized and
        partial_update if user is allowed to perform the same
        """

        request_keys = request.data.keys()
        if not has_helpcentre_rights(request.user):
            if 'assignees' in request_keys or 'is_closed' in request_keys:
                return Response(
                    data={
                        'Error': 'You cannot perform this operation.'
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        # Notifications start

        request_person = self.request.person
        query_id = request.data.get('id')
        query = Query.objects.get(id=query_id)
        category_obj = get_base_category()
        url = f'/helpcentre/issue/{query_id}'

        # For query status related notification
        if 'is_closed' in request.data.keys():
            if query.is_closed != request.data['is_closed']:
                if request.data['is_closed'] is True:
                    status = 'closed'
                else:
                    status = 'open'
                template = f'Your query {query.title} has been marked {status}'
                person_id = query.uploader.id
                push_notification(
                    template=template,
                    category=category_obj,
                    web_onclick_url=url,
                    person=person_id,
                    is_personalised=True
                )

        # For assignee related notification
        if 'assignees' in request.data.keys():
            new_assignees = request.data['assignees']
            old_assignees = list(query.assignees.all().values_list(
                'id', flat=True)
            )
            is_added = None
            assignee_id = None
            for maintainer_id in new_assignees:
                if assignee_id is not None:
                    break
                if maintainer_id not in old_assignees:
                    is_added = True
                    assignee_id = maintainer_id
                    break
            for maintainer_id in old_assignees:
                if assignee_id is not None:
                    break
                if maintainer_id not in new_assignees:
                    is_added = False
                    assignee_id = maintainer_id
                    break
            status = 'assigned to' if is_added is True else 'unassigned from'
            common_assignees = [
                id for id in new_assignees if id in old_assignees
            ]

            # For the fellow assignees
            person = Maintainer.objects.get(id=assignee_id).person
            person_ids = [
                Maintainer.objects.get(id=maintainer_id).person_id
                for maintainer_id in common_assignees
            ]
            person_ids = [
                id for id in person_ids if id != request_person.id
            ]
            template = (
                f'{person.full_name} has been {status} query '
                f'{query.title} opened by {query.uploader.full_name}'
                f' for app {query.app_name}'
            )
            if person_ids:
                push_notification(
                    template=template,
                    category=category_obj,
                    web_onclick_url=url,
                    persons=person_ids,
                    has_custom_users_target=True
                )

            # For the query opener
            if is_added is not None and query.uploader_id != request_person.id:
                template = f'{person.full_name} has been {status} your query {query.title}'
                person_id = query.uploader_id
                push_notification(
                    template=template,
                    category=category_obj,
                    web_onclick_url=url,
                    person=person_id,
                    is_personalised=True
                )

            # For the newly assigned/unassigned maintainer
            person_id = Maintainer.objects.get(id=assignee_id).person_id
            if person_id != request_person.id:
                template = (
                    f'You have been {status} query {query.title} '
                    f'opened by {query.uploader.full_name}'
                    f' for app {query.app_name}'
                )
                push_notification(
                    template=template,
                    category=category_obj,
                    web_onclick_url=url,
                    person=person_id,
                    is_personalised=True
                )

        # Notifications end

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

            # Notifications start

            url = f'/helpcentre/issue/{query_id}'
            category_obj = get_base_category()
            person_ids = list(query.assignees.all().values_list(
                'person_id',
                flat=True
            ))
            person_ids = [
                id for id in person_ids if id != person.id
            ]
            template = (
                f'{person.full_name} added a comment on '
                f'{query.uploader.full_name}\'s query {query.title}'
            )

            # For fellow assignees
            if person_ids:
                push_notification(
                    template=template,
                    category=category_obj,
                    web_onclick_url=url,
                    persons=person_ids,
                    has_custom_users_target=True
                )

            # For the uploader
            if query.uploader_id != person.id:
                uploader_id = query.uploader_id
                template = (
                    f'{person.full_name} added a '
                    f'comment on your query {query.title}'
                )
                push_notification(
                    template=template,
                    category=category_obj,
                    web_onclick_url=url,
                    person=uploader_id,
                    is_personalised=True
                )

            # Notifications end

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                data={
                    'Error': 'You cannot perform this operation.'
                },
                status=status.HTTP_403_FORBIDDEN,
            )
