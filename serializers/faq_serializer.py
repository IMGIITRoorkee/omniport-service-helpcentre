from helpcentre.models import Faq
from rest_framework import serializers


class FaqSerializer(serializers.ModelSerializer):

    class Meta:
        model = Faq
        fields = ('id', 'app_name', 'question', 'answer')
