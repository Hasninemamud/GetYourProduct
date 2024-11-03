from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Category, Profile, Product, Order, Cart, CartItem

# Profile Admin
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image', ]
    search_fields = ['user__username', 'user__email']
    readonly_fields = []

# Product Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', ]
    list_filter = []
    search_fields = ['name', 'description']
    ordering = []

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category']

# Order Admin
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity','confirmed', 'ordered_date']
    list_filter = [ 'ordered_date']
    list_editable = ('confirmed',)
    search_fields = ['user__username', 'product__name']
    ordering = ['ordered_date']

# Cart Admin
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', ]
    search_fields = ['user__username']
    ordering = []

# CartItem Admin
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']
    list_filter = ['product']
    search_fields = ['cart__user__username', 'product__name']



# Extend User Admin to include Profile in User management
class UserProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]

# Unregister and reregister User to add profile inline
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register other models with their custom admins
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
