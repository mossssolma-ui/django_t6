from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect

from catalog.models import Product, Category


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


def product_add(request: HttpRequest) -> HttpResponse | None:
    """ Функция для добавления нового продукта """
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            descriptions = request.POST.get("descriptions", '')
            category_id = request.POST.get("category_id")
            price = request.POST.get("price", 0)

            if not name or not category_id or not price:
                return HttpResponse("Обязательные поля не заполнены", status=400)

            product = Product.objects.create(
                name=name,
                descriptions=descriptions,
                category_id=category_id,
                price=price,
            )

            if request.FILES.get("image"):
                product.image = request.FILES.get("image")
                product.save()

            return redirect('catalog:products_list')

        except Exception as e:
            return HttpResponse("Ошибка при создании продукта")

    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "catalog/product_add.html", context=context)
