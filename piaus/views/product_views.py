from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from piaus.models import Products
from piaus.serializers import ProductsSerializer


from rest_framework import status


# Create your views here.


@api_view(['GET'])
def getProducts(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''

    products = Products.objects.filter(
        name__icontains=query).order_by('-createdAt')

    page = request.query_params.get('page')
    paginator = Paginator(products, 8)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = ProductsSerializer(products, many=True)
    return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})




@api_view(['GET'])
def getTopProducts(request):
    products = Products.objects.filter(rating__gte=4).order_by('-rating')[0:5]
    serializer = ProductsSerializer(products, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def getProduct(request, pk):
    product = Products.objects.get(_id=pk)
    serializer = ProductsSerializer(product, many=False)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    user = request.user

    product = Products.objects.create(
        user=user,
        name='Sample Name',
        price=0,
        brand='Sample Brand',
        countInStock=0,
        category='Sample Category',
        description=''
    )

    serializer = ProductsSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    data = request.data
    product = Products.objects.get(_id=pk)

    product.name = data['name']
    product.price = data['price']
    product.brand = data['brand']
    product.countInStock = data['countInStock']
    product.category = data['category']
    product.description = data['description']

    product.save()

    serializer = ProductsSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    product = Products.objects.get(_id=pk)
    product.delete()
    return Response('Producted Deleted')

@api_view(['POST'])
def uploadImage(request):
    data = request.data

    product_id = data['product_id']
    product = Products.objects.get(_id=product_id)

    product.image = request.FILES.get('image')
    product.save()

    return Response('Image was uploaded')