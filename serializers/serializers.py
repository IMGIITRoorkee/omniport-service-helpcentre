import swapper
from rest_framework import serializers

from kernel.serializers.root import ModelSerializer
from kernel.serializers.person import AvatarSerializer
from kernel.serializers.roles.maintainers import MaintainerSerializer

from comments.serializers import CommentSerializer

from helpcentre.models import Query

Maintainer = swapper.load_model('kernel', 'Maintainer')


class QuerySerializer(ModelSerializer):
    """
    Serializer for the Query Model
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
        This overrides the create method. This function remove the assignee and
        is_closed parameters from request.
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
        Meta class for Query Serializer class
        """

        model = Query
        exclude = (
            'removed',
            'datetime_created',
            'comments',
        )
        read_only = (
            'id',
            'uploader',
        )
        depth = 1


class QueryDetailSerializer(QuerySerializer):
    """
    Serializer for the Detailed Query
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
        Meta class for QueryDetailSerializer class
        """

        model = Query
        exclude = (
            'removed',
            'datetime_created',
        )
        read_only = (
            'id',
            'uploader',
        )
        depth = 1
