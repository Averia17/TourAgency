from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from images.serializers import ImageSerializer
from locations.models import City, Continent, Country, Destination


class DestinationSerializer(ModelSerializer):
    image = ImageSerializer(read_only=True)
    country = PrimaryKeyRelatedField(queryset=Country.objects.all(), write_only=True)

    class Meta:
        model = Destination
        fields = (
            "id",
            "name",
            "longitude",
            "latitude",
            "image",
            "description",
            "country",
        )


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
        model = Continent
        fields = ("id", "name", "countries")
