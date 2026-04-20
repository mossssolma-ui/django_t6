from django import forms

from .models import Product, Category


class StyleFormMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            fild.widget.attrs["class"] = "form-control"


class ProductForm(StyleFormMixin, forms.ModelForm):
    excluded_words = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]

    class Meta:
        model = Product
        fields = ["name", "descriptions", "image", "category", "price"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        name_lower = name.lower()

        for word in self.excluded_words:
            if word in name_lower:
                raise forms.ValidationError(f"Название содержит запрещенное слово {word}")

        return name

    def clean_descriptions(self):
        descriptions = self.cleaned_data.get("descriptions")
        descriptions_lower = descriptions.lower()

        for word in self.excluded_words:
            if word in descriptions_lower:
                raise forms.ValidationError(f"Описание содержит запрещенное слово {word}")

        return descriptions

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной")

        return price

    def clean_image(self):
        image = self.cleaned_data.get("image")

        valid_format_file = ["jpeg", "png"]
        valid_format_image = image.name.split(".")[-1].lower()
        if valid_format_image not in valid_format_file:
            raise forms.ValidationError(
                f'Поддерживаются форматы: {" ".join(valid_format_file)}. ' f"Ваш формат: {valid_format_image}"
            )

        max_size = 5 * 1024 * 1024
        if image.size > max_size:
            raise forms.ValidationError(f"Максимальный размер изображения не должен превышать 5мб")

        return image


class CategoryForm(StyleFormMixin, forms.ModelForm):
    excluded_words = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]

    class Meta:
        model = Category
        fields = ["name", "descriptions"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        name_lower = name.lower()

        for word in self.excluded_words:
            if word in name_lower:
                raise forms.ValidationError(f"Название категории содержит запрещенное слово {word}")

        return name

    def clean_descriptions(self):
        descriptions = self.cleaned_data.get("descriptions")
        descriptions_lower = descriptions.lower()

        for word in self.excluded_words:
            if word in descriptions_lower:
                raise forms.ValidationError(f"Описание содержит запрещенное слово {word}")

        return descriptions
