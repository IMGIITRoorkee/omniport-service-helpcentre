from rest_framework.serializers import ModelSerializer
from helpcentre.models import faq

class faq_serializer(ModelSerializer):
    class Meta:
        model=faqfields='__all__'