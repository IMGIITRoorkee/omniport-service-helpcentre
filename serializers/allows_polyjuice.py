from rest_framework import serializers

from base_auth.managers.get_user import get_user
from base_auth.models import User


class AllowsPolyjuiceSerializer(serializers.Serializer):
    """
    Stores the user who want to allow Polyjuice access to a maintainer
    """

    allows_polyjuice = serializers.BooleanField(required=True)
