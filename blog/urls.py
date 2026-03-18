from django.urls import path
from blog.apps import BlogConfig
from . import views

app_name = BlogConfig.name

urlpatterns = [
    path("", views.BlogPostListView.as_view(), name="post_list"),
    path("post_details/<int:pk>/", views.BlogPostDetailView.as_view(), name="post_details"),
    path("post_create/", views.BlogPostCreateView.as_view(), name="post_create"),
    path("update/<int:pk>/", views.BlogPostUpdateView.as_view(), name="post_update"),
    path("delete/<int:pk>/", views.BlogPostDeleteView.as_view(), name="post_delete"),
]
