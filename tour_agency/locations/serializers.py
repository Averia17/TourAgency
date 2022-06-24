from rest_framework.serializers import ModelSerializer

from locations.models import City, Continent, Country


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name", "longitude", "latitude")


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "name")


class ContinentSerializer(ModelSerializer):
    class Meta:
        model = Continent
        fields = ("id", "name")


class ContinentDetailSerializer(ContinentSerializer):
    countries = CountrySerializer(many=True)

    class Meta(ContinentSerializer.Meta):
        fields = ContinentSerializer.Meta.fields + ("countries",)
