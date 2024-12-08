from django.contrib.auth.views import LogoutView

from .views import *
from django.urls import path

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('', ProductListViewSet.as_view({'get': 'list',
                                     'post': 'create'}), name='product_list'),
    path('<int:pk>/', ProductDetailViewSet.as_view({'get': 'retrieve',
                                              'put':'update',
                                              'delete': 'destroy'}), name='product_detail'),

    path('', CategoryViewSet.as_view({'get': 'list',
                                     'post': 'create'}), name='category_list'),
    path('category/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve',
                                              'put': 'update',
                                              'delete': 'destroy'}), name='category_detail'),

    path('user/', UserProfileListViewSet.as_view({'get': 'list',
                                     'post': 'create'}), name='user_list'),
    path('user/<int:pk>/', UserProfileDetailViewSet.as_view({'get': 'retrieve',
                                              'put': 'update',
                                              'delete': 'destroy'}), name='user_detail'),

    path('', RatingViewSet.as_view({'get': 'list',
                                     'post': 'create'}), name='rating_list'),
    path('rating/<int:pk>/', RatingViewSet.as_view({'get': 'retrieve',
                                              'put': 'update',
                                              'delete': 'destroy'}), name='rating_detail'),

    path('', ReviewViewSet.as_view({'get': 'list',
                                     'post': 'create'}), name='review_list'),
    path('review/<int:pk>/', ReviewViewSet.as_view({'get': 'retrieve',
                                              'put': 'update',
                                              'delete': 'destroy'}), name='review_detail'),
]