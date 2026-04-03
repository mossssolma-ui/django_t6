from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView

from catalog.forms import ProductForm
from catalog.models import Product, Category


class ProductListView(ListView):
    """Класс для отображения списка продуктов"""

    model = Product
    template_name = "catalog/products_list.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    """Класс для отображения данных конкретного продукта"""

    model = Product
    template_name = "catalog/product_details.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
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


class ProductUpdateView(UpdateView):
    """Класс для изменения продукта"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:products_list")

    def get_context_data(self, **kwargs):
        """для добавления всех категорий в контекст"""
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class ProductDeleteView(DeleteView):
    """Класс для удаления продукта"""

    model = Product
    template_name = "catalog/product_delete.html"
    success_url = reverse_lazy("catalog:products_list")


class ContactsView(TemplateView):
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
