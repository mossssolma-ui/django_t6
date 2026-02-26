from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    """Функция рендерит главную html-страницу"""
    return render(request, "catalog/home.html")


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
