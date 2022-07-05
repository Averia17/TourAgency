from rest_framework.serializers import ModelSerializer

from images.serializers import ImageSerializer
from locations.models import City, Continent, Country, Destination


class DestinationSerializer(ModelSerializer):
    class Meta:
        model = Destination
        fields = ("id", "name", "longitude", "latitude")


class CitySerializer(DestinationSerializer):
    class Meta(DestinationSerializer.Meta):
        model = City


class CountrySerializer(ModelSerializer):
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = Country
        fields = ("id", "name", "images")


class ContinentDetailSerializer(ModelSerializer):
    countries = CountrySerializer(many=True)

    class Meta:
        fields = ("id", "name", "countries")
