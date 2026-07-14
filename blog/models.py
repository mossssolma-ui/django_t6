from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=50, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое")
    image = models.ImageField(upload_to="blog_photos/", blank=True, null=True, verbose_name="Изображение")
    is_published = models.BooleanField(verbose_name="Опубликовано", default=False)
    count_views = models.IntegerField(verbose_name="Просмотры", default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-created_at"]
