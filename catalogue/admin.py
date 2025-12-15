

from django.contrib import admin
from django import forms
from .models import MedicineDetail
from django.utils.html import format_html
from .models import OfferedRates

# Custom admin form to make ingredients easy to enter
class MedicineDetailAdminForm(forms.ModelForm):
    ingredients_text = forms.CharField(
        widget=forms.Textarea(attrs={'rows':5, 'cols':40}),
        required=False,
        help_text="Enter one ingredient per line like: Calcium:500mg"
    )

    class Meta:
        model = MedicineDetail
        fields = '__all__'  # include JSONField, don't exclude it

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-fill ingredients_text from JSONField if it exists
        if self.instance and self.instance.ingredients:
            lines = [f"{i['ingredient']}:{i['amount']}" for i in self.instance.ingredients]
            self.fields['ingredients_text'].initial = "\n".join(lines)
        # Image preview
        if self.instance and self.instance.image:
            self.fields['image'].help_text = format_html(
                '<img src="{}" style="height:100px;" />', self.instance.image.url
            )

    def save(self, commit=True):
        # Convert ingredients_text to JSON before saving
        instance = super().save(commit=False)
        text = self.cleaned_data.get('ingredients_text', '')
        ingredients_list = []
        if text:
            for line in text.splitlines():
                if ":" in line:
                    name, amount = line.split(":", 1)
                    ingredients_list.append({"ingredient": name.strip(), "amount": amount.strip()})
        instance.ingredients = ingredients_list
        if commit:
            instance.save()
        return instance

# Admin class
class MedicineDetailAdmin(admin.ModelAdmin):
    form = MedicineDetailAdminForm
    list_display = ('name', 'formulation', 'MRP', 'image_tag')
    search_fields = ('name', 'formulation')
    list_filter = ('formulation',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:100px;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'

# Register the model
admin.site.register(MedicineDetail, MedicineDetailAdmin)


admin.site.register(OfferedRates)

