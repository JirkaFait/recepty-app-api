from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe, RecipIngredient, Units


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag object"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_Fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for an ingredient object"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class UnitsSerializer(serializers.ModelSerializer):
    """Serializer for an ingredient object"""

    class Meta:
        model = Units
        fields = ('id', 'name', 'title')
        read_only_fields = ('id',)


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    unit = UnitsSerializer(read_only=True)
    ingredient = IngredientSerializer(read_only=True)

    class Meta:
        model = RecipIngredient
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""
    ingredients = RecipeIngredientsSerializer(read_only=True, many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'title', 'tags', 'time_minutes', 'price',
            'link', 'ingredients',
        )
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    # ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)


class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to recipe"""

    class Meta:
        model = Recipe
        fields = ('id', 'image')
        read_only_fields = ('id',)
