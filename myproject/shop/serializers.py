from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone', 'status', 'data_registration')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверные учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class UserProfileDetailSerializer(serializers.ModelSerializer):
    data_registration = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'age', 'phone', 'email',
                  'user_image', 'status', 'data_registration']


class CategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name',]


class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ['image',]



class RatingSerializer(serializers.ModelSerializer):
    user = UserProfileListSerializer()

    class Meta:
        model = Rating
        fields = ['user', 'stars']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserProfileListSerializer()

    class Meta:
        model = Review
        fields = ['user', 'date', 'text']


class ProductListSerializer(serializers.ModelSerializer):
    owner = UserProfileListSerializer()
    photos = ProductPhotoSerializer(many=True, read_only=True)
    get_avr_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField


    class Meta:
        model = Product
        fields = ['id', 'product_name', 'photos', 'price',
                   'owner', 'get_avr_rating', 'get_count_people']

    def get_avr_rating(self, obj):
        return obj.get_avr_rating()


    def get_count_people(self, obj):
        return obj.get_count_people()

class CategorySerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['category_name', 'products']


class ProductDetailSerializer(serializers.ModelSerializer):
    owner = UserProfileListSerializer()
    photos = ProductPhotoSerializer(many=True, read_only=True)
    category = CategorySimpleSerializer()
    created_date = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))
    ratings = RatingSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['category', 'product_name','description', 'price', 'check_original',
                 'product_video', 'photos', 'created_date',  'owner', 'ratings', 'reviews']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')

    class Meta:
        model = CarItem
        fields = ['id', 'product', 'product_id', 'quantity', 'get_total_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()
