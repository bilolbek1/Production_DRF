from rest_framework import serializers

from .models import Warehouse, Material

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['name']  # Materialning kerakli maydonlarini qo'shing


#Bu serializer omborxonadagi xomashyolar malumotlarini chiqarish uchun
class WarehouseSerializer(serializers.ModelSerializer):
    material_id = MaterialSerializer(read_only=True)  # MaterialSerializer dan foydalanamiz

    class Meta:
        model = Warehouse
        fields = ('id', 'material_id', 'remainder', 'price')  # Warehouse modelining kerakli maydonlari


