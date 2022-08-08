from django.contrib import admin
from .models import Food, Category

# class FoodAdmin(admin.ModelAdmin):
#   list_per_page = 20 # 딱히 적용 안되는듯?
# #   readonly_fields = ('created_at', 'updated_at')

# class CategoryAdmin(admin.ModelAdmin):
#   # 작성 시 필드가 자동으로 채워지도록 설정
#   prepopulated_fields = {'slug' : ('name', )}

# admin.site.register(Food, FoodAdmin)
# admin.site.register(Category, CategoryAdmin)

admin.site.register(Food)
admin.site.register(Category)