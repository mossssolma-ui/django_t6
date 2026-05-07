from .models import Category, Product


class ProductService:

    @staticmethod
    def get_category_name(category_id):
        category = Category.objects.get(id=category_id)
        if not category:
            return None
        return category.name

    @staticmethod
    def get_products(category_id):
        products = Product.objects.filter(category_id=category_id)
        if not products.exists():
            return None
        return products
