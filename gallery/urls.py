from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView, name='product-list'),
    path('<str:pk>/details/', views.ProductDetailView.as_view(), name='product-detail'),
    path('create/', views.ProductCreateView.as_view(), name='product-create'),
    path('update/<str:pk>/', views.product_edit_view, name='product-update'),
    path('delete/<str:pk>/', views.product_delete, name='product-delete'),
    path('signup/', views.create_user, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.login_user, name='logout'),
]
