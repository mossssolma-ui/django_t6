from django.urls import path
from catalog.apps import CatalogConfig
from . import views

app_name = CatalogConfig.name

urlpatterns = [
    path("", views.products_list, name="products_list"),
    path("contacts/", views.contacts, name="contacts"),
    path("product_details/<int:product_id>", views.product_details, name="product_details"),
]
