from rest_framework.serializers import ModelSerializer
from helpcentre.models import quickguide

class quickguide_serializer(ModelSerializer):
    class Meta:
        model=quickguide
        fields='__all__'