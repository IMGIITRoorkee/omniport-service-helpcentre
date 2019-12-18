import swapper
from rest_framework import serializers

from comments.serializers import CommentSerializer
from formula_one.serializers.base import ModelSerializer
from helpcentre.models import Query
from kernel.serializers.person import AvatarSerializer
from omniport.utils import switcher

Maintainer = swapper.load_model('kernel', 'Maintainer')
MaintainerSerializer = switcher.load_serializer('kernel', 'Maintainer')


class QuerySerializer(ModelSerializer):
    """
    Serializer for the Query model
    """

    uploader = AvatarSerializer(
        read_only=True,
    )

    assignees = serializers.PrimaryKeyRelatedField(
        queryset=Maintainer.objects.all(),
        many=True,
    )

    def create(self, validated_data):
        """
        Overrides the create method to remove the parameters `assignees` and
        `is_closed` from request.
        :param validated_data: validated_data by serializer
        :return: created instance of Query
        """

        request_keys = validated_data.keys()

        if 'assignees' in request_keys:
            validated_data.pop('assignees')
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
            'comments',
        ]
        read_only = [
            'id',
            'datetime_created',
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

    assignees = MaintainerSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        """
        Meta class for QueryDetailSerializer
        """

        model = Query
        exclude = [
            'datetime_modified'
        ]
        read_only = [
            'id',
            'datetime_created',
            'uploader',
        ]
        depth = 1
