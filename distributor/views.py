from django.contrib import auth
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from distributor.models import Product, Review, HashTag
from .serializers import ProductListSerializer, ReviewListSerializer, TagValidateSerializer, ProductValidateSerializer, \
    UserLoginValidateSerializer, UserRegisterValidateSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def product_list_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = ProductListSerializer(products, many=True).data
        return Response(data={'list': data})
    elif request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    'massage': 'ERROR',
                    'error': serializer.errors
                })
        product = Product.objects.create(
            name=serializer.validated_data['name'],
            price=serializer.validated_data['price'],
            quantity=serializer.validated_data['quantity'],
            descriptor=serializer.validated_data['description'],
        )
        product.HashTag.set(serializer.validated_data['tags'])
        product.save()
        return Response()


@api_view(['GET'])
def product_item_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        raise NotFound('Товар не найден')
    data = ProductListSerializer(product, many=False).data
    return Response(data=data)


@api_view(['GET'])
def review_list(request):
    reviews = Review.objects.all()
    data = ReviewListSerializer(reviews, many=True).data
    return Response(data=data)


@api_view(['POST'])
def tag_create(request):
    serializer = TagValidateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            status=status.HTTP_406_NOT_ACCEPTABLE,
            data={
                'massage': 'ERROR',
                'errors': serializer.errors
            }
        )
    name = request.data.get('hash_tag', '')
    HashTag.objects.create(name=name)
    return Response(data={'massage': 'created'})


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = UserLoginValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    'massage': 'error',
                    'errors': serializer.errors
                }
            )
        username = request.data['username']
        password = request.data['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.get(user=user)
            return Response(data={'key': token.key})
        else:
            return Response(data={'massage': 'USER NOT FOUND'})


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserRegisterValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    'massage': 'error',
                    'errors': serializer.errors
                }
            )
    User.objects.create_user(
        request.data['username'],
        email='a@n.ru',
        password=request.data['password']
    )
    return Response(data={'massage': 'USER CREATED'})
