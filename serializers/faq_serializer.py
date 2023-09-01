from rest_framework.serializers import ModelSerializer
from helpcentre.models import faq

class FaqSerializer(ModelSerializer):
    class Meta:
        model=faq
        fields='__all__'
        