from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView

from catalog.forms import ProductForm, CategoryForm, ProductModeratorForm
from catalog.models import Product, Category
from .services import ProductService


class ProductListView(ListView):
    """Класс для отображения списка продуктов"""

    model = Product
    template_name = "catalog/products_list.html"
    context_object_name = "products"

    def get_queryset(self):
        """
        Получает данные по продуктам из кэша,
        если кэш пуст, получает данные из БД
        """
        queryset = cache.get("products_list_queryset")
        if not queryset:
            queryset = super().get_queryset()
            cache.set("products_list_queryset", queryset, 60 * 15)
        return queryset


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Класс для отображения данных конкретного продукта"""

    model = Product
    template_name = "catalog/product_details.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Класс для создания нового продукта"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:products_list")

    def get_context_data(self, **kwargs):
        """для добавления всех категорий в контекст"""
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def form_valid(self, form):
        """Автоматически назначаем владельца продукта"""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Класс для изменения продукта"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:products_list")

    def post(self, request, *args, **kwargs):
        """Ручная обработка POST запроса с чекбоксом"""
        self.object = self.get_object()

        name = request.POST.get("name")
        descriptions = request.POST.get("descriptions")
        price = request.POST.get("price")
        category_id = request.POST.get("category")

        is_published = request.POST.get("is_published") == "on"

        self.object.name = name
        self.object.descriptions = descriptions
        self.object.price = price
        self.object.category_id = category_id
        self.object.is_published = is_published
        self.object.save()

        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        """для добавления всех категорий в контекст"""
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def get_form_class(self):
        """Показ пользователю формы в зависимости от доступа"""
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm("catalog.can_unpublish_product"):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Класс для удаления продукта"""

    model = Product
    template_name = "catalog/product_delete.html"
    success_url = reverse_lazy("catalog:products_list")

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        user = request.user

        if user == product.owner or user.has_perm("catalog.delete_product"):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("У вас нет прав на удаление продукта")


class ProductCategoryView(LoginRequiredMixin, ListView):
    """Класс для отображения продуктов определенной категории"""

    template_name = "catalog/products_category.html"
    context_object_name = "products"

    def get_queryset(self):
        category_id = self.kwargs.get("pk")
        return ProductService.get_products(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("pk")
        context["category_name"] = ProductService.get_category_name(category_id)
        return context


class CategoryListView(LoginRequiredMixin, ListView):
    """Класс для отображения списка категории"""

    model = Category
    template_name = "catalog/category_list.html"
    context_object_name = "categories"


class CategoryDetailView(LoginRequiredMixin, DetailView):
    """Класс для отображения данных категории"""

    model = Category
    template_name = "catalog/category_details.html"
    context_object_name = "category"


class CategoryCreateView(LoginRequiredMixin, CreateView):
    """Класс для создания новой категории"""

    model = Category
    form_class = CategoryForm
    template_name = "catalog/category_form.html"
    success_url = reverse_lazy("catalog:category_list")


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    """Класс для изменения категории"""

    model = Category
    form_class = CategoryForm
    template_name = "catalog/category_form.html"
    success_url = reverse_lazy("catalog:category_list")


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    """Класс для удаления категории"""

    model = Category
    template_name = "catalog/category_delete.html"
    success_url = reverse_lazy("catalog:category_list")


class ContactsView(LoginRequiredMixin, TemplateView):
    """Класс для отображения контактов и обработки формы"""

    template_name = "catalog/contacts.html"

    def post(self, request, *args, **kwargs):
        """Обрабатывает POST-запрос (отправку формы)"""
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        return HttpResponse(
            f"Спасибо, {name}! Сообщение длиной = {len(message)} знаков получено. "
            f"Ответ пришлем на эту почту {email}"
        )
