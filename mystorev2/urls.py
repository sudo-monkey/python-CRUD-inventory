from os import name
from . import views
from django.conf.urls import include, url
from django.urls import path, include
from mystorev2.views import Dashboard, RegistrationView, AdminView, AdminGroupList, AdminGroupUpdate, admindb
from .views import AdminUpdate, LandingView, WarehouseCreate, WarehouseList, WarehouseUpdate, WarehouseDelete
from .views import ProductCreate, ProductList, ProductUpdate, ProductDelete
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = 'mystorev2'

urlpatterns = [

    # Path for authentication
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^admindb/", admindb, name="admindb"),


    # Path for Dashboard
    path("", WarehouseList.as_view(), name='dashboard'),
    path("landing/", LandingView.as_view(), name='landing'),


    # CRUD for Warehouse
    path("add-wh/", WarehouseCreate.as_view(), name='new-warehouse'),
    path("view-wh/", WarehouseList.as_view(), name='whls'),
    path("<int:pk>/update-wh/",
         WarehouseUpdate.as_view(), name='warehouse-update'),
    path("<int:pk>/delete-wh/",
         WarehouseDelete.as_view(), name='warehouse-delete'),

    # CRUD for Product
    path("add-pd/", ProductCreate.as_view(), name='new-product'),
    path("view-pd/", ProductList.as_view(), name='pdls'),
    path("<int:pk>/update-pd/",
         ProductUpdate.as_view(), name='product-update'),
    path("<int:pk>/delete-pd/",
         ProductDelete.as_view(), name='warehouse-delete'),

    # RBAC
    path("register/", RegistrationView.as_view(), name='register'),
    path("management/", AdminView.as_view(), name='management'),
    path("management/<int:pk>/managementaccess/",
         AdminUpdate.as_view(), name='edit-access'),
    path("management/groupaccess/",
         AdminGroupList.as_view(), name='view-group-access'),
    path("management/groupaccess/<int:pk>",
         AdminGroupUpdate.as_view(), name='update-group-access'),
    #     path("management/<int:pk>/groupaccess/",
    #          AdminGroupUpdate.as_view(), name='edit-group-access'),
    #     path("management/static", static_html, name='static'),



]

urlpatterns += staticfiles_urlpatterns()
