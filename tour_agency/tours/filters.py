from django_filters import rest_framework as filters, Filter

from core.constants import TOUR_TYPES
from tours.models import Tour


class ListFilter(Filter):
    def __init__(self, query_param, *args, **kwargs):
        super(ListFilter, self).__init__(*args, **kwargs)
        self.query_param = query_param
        self.lookup_expr = "in"

    def filter(self, queryset, value):
        try:
            request = self.parent.request
        except AttributeError:
            return None

        values = set()
        query_list = request.GET.getlist(self.query_param)
        for v in query_list:
            values = values.union(set(v.split(",")))
        values = set(map(str, values))
        if values:
            return super(ListFilter, self).filter(queryset, values)
        return queryset


class TourFilter(filters.FilterSet):
    destinations = ListFilter(
        field_name="tour_features__destination__name", query_param="destinations"
    )
    tour_type = filters.ChoiceFilter(field_name="tour_type", choices=TOUR_TYPES)

    class Meta:
        model = Tour
        fields = ["tour_type"]
