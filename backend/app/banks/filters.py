import django_filters as df
from .models import Bank

class BankFilter(df.FilterSet):
    min_rating = df.NumberFilter(field_name="rating", lookup_expr="gte")
    max_rating = df.NumberFilter(field_name="rating", lookup_expr="lte")
    country = df.CharFilter(field_name="country", lookup_expr="iexact")
    is_active = df.BooleanFilter()

    class Meta:
        model = Bank
        fields = ["country","is_active","min_rating","max_rating"]
