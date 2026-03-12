from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404

from catalog.models import Product


def contacts(request: HttpRequest) -> HttpResponse:
    """Функция обрабатывает POST, рендерит html-страницу с контактными данными"""
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        return HttpResponse(
            f"Спасибо, {name}! Сообщение длиной = {len(message)} знаков получено. Ответ пришлем на эту почту {email}"
        )
    return render(request, "catalog/contacts.html")


def products_list(request: HttpRequest) -> HttpResponse:
    """ Функция вывода продукта """
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "catalog/products_list.html", context=context)


def product_details(request: HttpRequest, product_id: int) -> HttpResponse:
    """ Функция будет возращать подробную информацию о продукте """
    product = get_object_or_404(Product, id=product_id)
    context = {"product": product}

    return render(request, "catalog/product_details.html", context=context)
