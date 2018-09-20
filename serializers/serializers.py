from rest_framework import serializers

from kernel.serializers.root import ModelSerializer
from kernel.serializers.person import AvatarSerializer
from kernel.serializers.roles.maintainers import MaintainerSerializer

from comments.serializers import CommentSerializer

from helpcentre.models import Query


class QuerySerializer(ModelSerializer):
    """
    Serializer for the Query Model
    """

    uploader = AvatarSerializer(
        read_only=True,
    )

    assignee = MaintainerSerializer(
        read_only=True,
        many=True,
    )

    comments = CommentSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        """
        Meta class for Query Serializer class
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
