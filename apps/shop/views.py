from django.http import Http404, HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, ProductCategory
from .serializer import ProductSerializer, ProductCategorySerializer


# Create your views here.


class ProductListCreateAPIView(APIView):

    @swagger_auto_schema(
        operation_summary='Get list of products',
        responses={
            '200': ProductSerializer(many=True),
        },
    )
    def get(self, request):
        product_qs = Product.objects.select_related('category').all()
        srz = ProductSerializer(product_qs, many=True)
        return Response(srz.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Create a product',
        request_body=ProductSerializer(many=False),
        responses={
            '201': ProductSerializer(many=False),
        },
    )
    def post(self, request):
        request_body = request.data
        new_product = Product.objects.create(
            name=request_body['name'], description=request_body['description'],
            price=request_body['price'])
        srz = ProductSerializer(new_product, many=False)
        return Response(srz.data, status=status.HTTP_201_CREATED)


class ProductRetrieveAPIView(APIView):

    @swagger_auto_schema(
        operation_summary='Get detail of product',
        responses={
            '200': ProductSerializer(many=False),
            '404': 'Product not found.',
        }
    )
    def get(self, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found.'},
                            status=status.HTTP_404_NOT_FOUND)
        srz = ProductSerializer(product, many=False)
        return Response(srz.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Delete a product',
        request_body=None,
        responses={'204': None}
    )
    def delete(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found.'},
                            status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_summary='Update detail of product',
        responses={
            '200': ProductSerializer(many=False),
        },
        request_body=ProductSerializer(many=False)
    )
    def put(self, request, pk):
        request_body = request.data
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            raise Http404
        product.name = request_body['name']
        product.description = request_body['description']
        product.price = request_body['price']
        product.save()

        srz = ProductSerializer(product, many=False)
        return Response(srz.data, status=status.HTTP_200_OK)


class CategoryListGetApiView(APIView):

    @swagger_auto_schema(
        operation_summary='Get list of categories',
        responses={
            '200': ProductSerializer(many=True),
        },
    )
    def get(self, request):
        try:
            category_qs = ProductCategory.objects.all()
        except ProductCategory.DoesNotExist:
            raise Http404
        category_srz = ProductCategorySerializer(category_qs, many=True)
        return Response(category_srz.data, status=status.HTTP_200_OK)


class CategoryRetrieveAPIView(APIView):

    @swagger_auto_schema(
        operation_summary='Get detail of categories',
        responses={
            '200': ProductCategorySerializer(many=False),
            '404': 'Category not found.',
        }
    )
    def get(self, pk):
        try:
            category = ProductCategory.objects.get(id=pk)
        except ProductCategory.DoesNotExist:
            return Response({'message': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)
        category_srz = ProductCategorySerializer(category, many=False)
        return Response(category_srz.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Create a product',
        request_body=ProductSerializer(many=False),
        responses={
            '201': ProductSerializer(many=False),
        },
    )
    def post(self, request):
        body = request.data
        category = ProductCategory.objects.create(title=body['title'], description=body['description'])
        category_srz = ProductCategorySerializer(category, many=False)
        return Response(category_srz.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='Delete category',
        request_body=None,
        responses={'204': None}
    )
    def delete(self, request, pk):
        try:
            category = ProductCategory.objects.get(id=pk)
        except ProductCategory.DoesNotExist:
            return Response({'message': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_summary='Update detail of category',
        responses={
            '200': ProductSerializer(many=False),
        },
        request_body=ProductSerializer(many=False)
    )
    def put(self, request, pk):
        body = request.data
        try:
            category = ProductCategory.objects.get(id=pk)
        except ProductCategory.DoesNotExist:
            raise Http404
        category.title = body['title']
        category.description = body['description']
        category.save()

        category_srz = ProductCategorySerializer(category, many=False)
        return Response(category_srz.data, status=status.HTTP_200_OK)







