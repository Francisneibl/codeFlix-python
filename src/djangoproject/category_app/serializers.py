from rest_framework import serializers


class CategorySerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    name = serializers.CharField(max_length=255, allow_blank=False)
    description = serializers.CharField()
    is_active = serializers.BooleanField(default=True)


class ListCategoriesResponseSerializer(serializers.Serializer):
    data = CategorySerializer(many=True)


class RetrieveCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class RetrieveCategoryResponseSerializer(serializers.Serializer):
    data = CategorySerializer(source="*")


class CreateCategoryRequestSerializer(CategorySerializer):
    pass


class CreateCategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateCategoryRequestSerializer(CategorySerializer):
    id = serializers.UUIDField()
    is_active = serializers.BooleanField()


class DeleteCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()

