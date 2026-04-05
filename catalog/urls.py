from django.urls import path
from catalog.apps import CatalogConfig
from . import views

app_name = CatalogConfig.name

urlpatterns = [
    path("", views.ProductListView.as_view(), name="products_list"),
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
    path("product/details/<int:pk>/", views.ProductDetailView.as_view(), name="product_details"),
    path("product/delete/<int:pk>/", views.ProductDeleteView.as_view(), name="product_delete"),
    path("product/add/", views.ProductCreateView.as_view(), name="product_add"),
    path("product/update/<int:pk>/", views.ProductUpdateView.as_view(), name="product_update"),
]
