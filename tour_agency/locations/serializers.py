from rest_framework.serializers import ModelSerializer

from locations.models import City


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = (
            "id",
            "name",
        )
