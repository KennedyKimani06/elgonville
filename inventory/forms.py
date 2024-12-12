from django import forms
from .models import InventoryItem, Supplier, Employee, Customer, Order, OrderItem

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'quantity', 'price_per_unit', 'supplier']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_information']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['user', 'position']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'contact_number']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', 'inventory_item', 'quantity', 'price']
