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

    path("category/list/", views.CategoryListView.as_view(), name="category_list"),
    path("category/details/<int:pk>/", views.CategoryDetailView.as_view(), name="category_details"),
    path("category/delete/<int:pk>/", views.CategoryDeleteView.as_view(), name="category_delete"),
    path("category/add/", views.CategoryCreateView.as_view(), name="category_add"),
    path("category/update/<int:pk>/", views.CategoryUpdateView.as_view(), name="category_update"),
]
