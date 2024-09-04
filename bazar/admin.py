from django.contrib.admin import register, ModelAdmin
from .models import *


@register(Asset)
class AssetAdmin(ModelAdmin):
    list_display = [
        'name'
    ]


@register(Sandogh)
class SandoghAdmin(ModelAdmin):
    pass