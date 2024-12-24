from django.urls import path
from .views import (UserControllerList, ProductControllerList, UserControllerDetail, ProductControllerDetail,
                    CartControllerDetail)

urlpatterns = [
    path('users/', UserControllerList.as_view()),
    path('products/', ProductControllerList.as_view()),
    path('users/<int:pk>/', UserControllerDetail.as_view()),
    path('products/<int:pk>/', ProductControllerDetail.as_view()),
    path('cart/<int:pk>', CartControllerDetail.as_view()),
]
