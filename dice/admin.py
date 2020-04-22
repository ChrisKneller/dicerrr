from django.contrib import admin
from .models import Upload, DiceImage, DiceTypes

# Register your models here.

admin.site.register(Upload)

class DiceImageAdmin(admin.ModelAdmin):
    list_display = ('image_id', 'uploaded_by', 'date_created', 'original_image', 'new_image', 'image_width', 'image_height', 'number_of_dice', 'construction_cost')

admin.site.register(DiceImage, DiceImageAdmin)

class DiceTypesAdmin(admin.ModelAdmin):
    list_display = ('dice_size', 'dice_cost')

admin.site.register(DiceTypes, DiceTypesAdmin)