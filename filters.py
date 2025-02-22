import django_filters
from MHS_app.models import *


class Product_filter(django_filters.FilterSet):
      Sub_category_id = django_filters.CharFilter(field_name='Sub_category_id')
      Price=django_filters.CharFilter(field_name='Price', lookup_expr='icontains')

      class Meta:
        model = Product
        fields = ['Price', 'Sub_category_id']


class Subcategory_filter(django_filters.FilterSet):
    Sub_Category_Name=django_filters.CharFilter(field_name='Sub_Category_Name',lookup_expr='icontains')

    class Meta:
        model=SubCategory
        fields=['Sub_Category_Name']


class Category_filter(django_filters.FilterSet):
    Category_name=django_filters.CharFilter(field_name='Category_name',lookup_expr='icontains')

    class Meta:
        model=Category
        fields=['Category_name'] 

class SubCategoryFilter(django_filters.FilterSet):
    product_price = django_filters.NumberFilter(field_name="products__Price", lookup_expr="gte")
    product_availability = django_filters.CharFilter(field_name="products__Availability", lookup_expr="icontains")

    class Meta:
        model = SubCategory
        fields = ["product_price", "product_availability"]  

        
                     