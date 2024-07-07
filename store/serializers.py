
from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id','title']
#    id = serializers.IntegerField()
#    title = serializers.CharField(max_length=255)
    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','unit_price','price_with_tax','collection']
#    id = serializers.IntegerField()
#    title = serializers.CharField(max_length=255)
#    price = serializers.DecimalField(
#        max_digits=6, decimal_places=2, source="unit_price")
#
#    # CUSTOME SERIALIZER
    price_with_tax = serializers.SerializerMethodField(
        method_name="calculate_tax")
#
#    collection = serializers.PrimaryKeyRelatedField(
#        queryset=Collection.objects.all()
#    )
#    collection = serializers.StringRelatedField()
#    collection = CollectionSerializer()
#    collection = serializers.HyperlinkedRelatedField(
#        queryset = Collection.objects.all(),
#        view_name= "collection-detail"
#    )
#
    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
