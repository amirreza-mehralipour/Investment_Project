from rest_framework.serializers import ModelSerializer
from .models import Sandogh, Asset

class SandoghSerializer(ModelSerializer):
    class Meta:
        model = Sandogh
        fields = '__all__'

class AssetSerializer(ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'

