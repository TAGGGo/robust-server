from re import template
from django.urls import path
from django.views.generic.base import TemplateView
from django.views.generic.base import RedirectView
from . import views
app_name = 'amazon'

urlpatterns = [
    path('signup/', TemplateView.as_view(template_name='signup.html')),
    path('login/', TemplateView.as_view(template_name='login.html')),
    path('account/', views.accountHandler, name="accountHandler"),
    path('store/', views.storePage, name="storePage"),
    path('index/', views.indexPage, name='indexPage'),
    path('products/<str:category>/', views.productsCategoryPage, name="productsPage"),
    path('products/', views.productsPage, name="productsPage"),
    path('signupHandler', views.signupHandler, name="register"),
    path('loginHandler', views.loginHandler, name="loginHandler"),
    path('logoutHandler', views.logoutHandler, name="logoutHandler"),
    path('updateProfile', views.updateProfile, name="updateProfile"),
    path('addToChart', views.addToChart, name="addToChart"),
    path('purchase', views.purchase, name="purchase"),
    path('cancelOrder', views.cancelOrder, name="purchase"),
    path('subscribe', views.subscribe, name="subscribe"),
    path('', RedirectView.as_view(url='/index',  permanent=False), name='index'),
]