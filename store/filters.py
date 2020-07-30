import django_filters
from django_filters import DateFilter, CharFilter,ModelChoiceFilter
from .models import *
from django import forms


class ProductFilter(django_filters.FilterSet):
    partial_name = CharFilter(
        field_name='name', lookup_expr='icontains',
        label="Name"
    )
    partial_description= CharFilter(
        field_name='description',lookup_expr='icontains',
        label='Description'
    )
    
    class Meta:
        model = Product
        fields = '__all__'
        exclude= ['seller','description','name','price']

class LocationFilter(django_filters.FilterSet):
    partial_name = CharFilter(
        field_name='name', lookup_expr='icontains',
        label='Name'
    )
    class Meta:
        model = Location
        fields = '__all__'
        exclude = ['seller','name']

class CustomerFilter(django_filters.FilterSet):
    partial_name = CharFilter(
        field_name='name', lookup_expr='icontains',
        label='Name'
    )
    class Meta:
        model = Location
        fields = []


def customers(request):
    print(request)
    if request is None:
        return Customer.objects.none()
    seller = request.user.seller
    return seller.customer_set.all()

def pickup_locations(request):
    if request is None:
        return Location.objects.none()
    seller = request.user.seller
    return seller.location_set.all()
    
class BasketFilter(django_filters.FilterSet):
    customer = ModelChoiceFilter(queryset=customers)
    pickup_location = ModelChoiceFilter(queryset=pickup_locations)

    class Meta:
        model = Basket
        fields= ['customer','pickup_location','status']
    

    