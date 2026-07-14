from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import BlogPost


class BlogPostListView(LoginRequiredMixin, ListView):
    """Класс для отображения списка постов"""

    model = BlogPost
    template_name = "blog/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Вывод только опубликованных"""
        queryset = super().get_queryset().filter(is_published=True)
        return queryset


class BlogPostDetailView(LoginRequiredMixin, DetailView):
    """Класс для отображения данных конкретного поста"""

    model = BlogPost
    template_name = "blog/post_details.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        """Увеличивает количество просмотров на 1"""
        obj = super().get_object(queryset)
        obj.count_views += 1
        obj.save()
        return obj


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    """Класс для создания поста"""

    model = BlogPost
    fields = ["title", "content", "image", "is_published", "count_views"]
    template_name = "blog/post_create.html"
    success_url = reverse_lazy("blog:post_list")
    context_object_name = "post"


class BlogPostUpdateView(LoginRequiredMixin, UpdateView):
    """Класс для изменения поста"""

    model = BlogPost
    fields = ["title", "content", "image", "is_published", "count_views"]
    template_name = "blog/post_create.html"
    context_object_name = "post"

    def get_success_url(self):
        """перенаправляет на отредактированный пост"""
        return reverse_lazy("blog:post_details", kwargs={"pk": self.object.pk})


class BlogPostDeleteView(LoginRequiredMixin, DeleteView):
    """Класс для удаления поста"""

    model = BlogPost
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")
