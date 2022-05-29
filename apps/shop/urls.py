from django.urls import path

from .views import ProductListCreateAPIView, ProductRetrieveAPIView, CategoryListGetApiView, CategoryRetrieveAPIView

urlpatterns = [
    path('products/', ProductListCreateAPIView.as_view()),
    path('products/<int:pk>/', ProductRetrieveAPIView.as_view()),
    path('categories/', CategoryListGetApiView.as_view()),
    path('categories/<int:pk>/', CategoryRetrieveAPIView.as_view()),
]