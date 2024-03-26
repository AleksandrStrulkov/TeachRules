from django.contrib import admin
from users.models import User


# Register your models here.
@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'avatar', 'phone', 'is_staff', 'is_active',
                    'date_joined', 'first_name', 'last_name')
    list_filter = ('email',)
    search_fields = ('email',)
