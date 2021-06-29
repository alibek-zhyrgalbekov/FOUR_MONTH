from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Product, Review, HashTag


class ReviewItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text rating'.split()


class ProductListSerializer(serializers.ModelSerializer):
    reviews = ReviewItemSerializer(many=True)
    reviews_count = serializers.SerializerMethodField()
    reviews1 = serializers.SerializerMethodField()
    hash_tag = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id name price reviews reviews1 reviews_count hash_tag'.split()

    def get_hash_tag(self, obj):
        return [i.name for i in obj.HashTag.all()]

    def get_reviews_count(self, obj):
        return obj.reviews.count()

    def get_reviews1(self, obj):
        reviews = Review.objects.filter(rating__gt=3, product=obj)
        data = ReviewItemSerializer(reviews, many=True).data
        return data


class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id name price'.split()


class ReviewListSerializer(serializers.ModelSerializer):
    product = ProductItemSerializer()

    class Meta:
        model = Review
        fields = 'id text rating product'.split()


class TagValidateSerializer(serializers.Serializer):
    hash_tag = serializers.CharField(min_length=2, max_length=255)

    def validate_hash_tag(self, obj):
        if HashTag.objects.filter(name=obj).count() > 0:
            raise ValidationError("Takoi hash teg uje sushestvuet!")


class ProductValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    price = serializers.FloatField()
    quantity = serializers.IntegerField()
    description = serializers.CharField(max_length=1000, default='', required=False)
    tags = serializers.ListField(child=serializers.IntegerField())


class UserLoginValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=1000)
    password = serializers.CharField(max_length=1000)


class UserRegisterValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=1000)
    password = serializers.CharField(max_length=1000)
    password1 = serializers.CharField(max_length=1000)

    def validate_username(self, username):
        if User.objects.filter(username=username).count() > 0:
            raise ValidationError("Пользователь уже существует")
