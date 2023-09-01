from rest_framework.serializers import ModelSerializer
from helpcentre.models import quickguide

class QuickguideSerializer(ModelSerializer):
    class Meta:
        model=quickguide
        fields='__all__'
        