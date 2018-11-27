import swapper
from rest_framework import serializers

from comments.serializers import CommentSerializer
from helpcentre.models import Query
from kernel.serializers.person import AvatarSerializer
from kernel.serializers.roles.maintainers import MaintainerSerializer
from kernel.serializers.root import ModelSerializer

Maintainer = swapper.load_model('kernel', 'Maintainer')


class QuerySerializer(ModelSerializer):
    """
    Serializer for the Query model
    """

    uploader = AvatarSerializer(
        read_only=True,
    )

    assignee = serializers.PrimaryKeyRelatedField(
        queryset=Maintainer.objects.all(),
        many=True,
    )

    def create(self, validated_data):
        """
        Overrides the create method to remove the parameters `assignee` and
        `is_closed` from request.
        :param validated_data: validated_data by serializer
        :return: created instance of Query
        """

        request_keys = validated_data.keys()

        if 'assignee' in request_keys:
            validated_data.pop('assignee')
        elif 'is_closed' in request_keys:
            validated_data.pop('is_closed')

        query = Query.objects.create(**validated_data)
        return query

    class Meta:
        """
        Meta class for QuerySerializer
        """

        model = Query
        exclude = [
            'removed',
            'datetime_created',
            'comments',
        ]
        read_only = [
            'id',
            'uploader',
        ]
        depth = 1


class QueryDetailSerializer(QuerySerializer):
    """
    Serializer for the detail view of Query viewset
    """

    comments = CommentSerializer(
        many=True,
        read_only=True,
    )

    assignee = MaintainerSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        """
        Meta class for QueryDetailSerializer
        """

        model = Query
        exclude = [
            'removed',
            'datetime_created',
        ]
        read_only = [
            'id',
            'uploader',
        ]
        depth = 1
