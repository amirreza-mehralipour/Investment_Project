from rest_framework.serializers import ModelSerializer
from .models import Sandogh

class sandoghSerializer(ModelSerializer):
    class Meta:
        model = Sandogh
        fields = '__all__'

