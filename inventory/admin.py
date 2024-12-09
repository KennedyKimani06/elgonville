from django.contrib import admin
from .models import InventoryItem, Supplier, Employee, Customer, Order, OrderItem
from accounts.forms import CustomUserCreationForm  # Import the form from accounts

class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'price_per_unit', 'supplier')

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_information')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'position')

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order_date', 'total_amount')
    inlines = [OrderItemInline]

admin.site.register(InventoryItem, InventoryItemAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
