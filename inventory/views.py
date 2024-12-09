from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import InventoryItem, Supplier, Employee, Customer, Order
from .forms import InventoryItemForm, SupplierForm, EmployeeForm, CustomerForm

def index(request):
    return render(request, 'inventory/index.html')

@login_required
def dashboard(request):
    return render(request, 'inventory/dashboard.html')

@login_required
def inventory_list(request):
    items = InventoryItem.objects.all()
    return render(request, 'inventory/inventory_list.html', {'items': items})

@login_required
def add_inventory(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory:inventory_list')
    else:
        form = InventoryItemForm()
    return render(request, 'inventory/add_inventory.html', {'form': form})

@login_required
def edit_inventory(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('inventory:inventory_list')
    else:
        form = InventoryItemForm(instance=item)
    return render(request, 'inventory/edit_inventory.html', {'form': form})

@login_required
def delete_inventory(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('inventory:inventory_list')
    return render(request, 'inventory/delete_inventory.html', {'item': item})

@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'inventory/employee_list.html', {'employees': employees})

@login_required
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory:employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'inventory/add_employee.html', {'form': form})

@login_required
def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('inventory:employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'inventory/edit_employee.html', {'form': form})

@login_required
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('inventory:employee_list')
    return render(request, 'inventory/delete_employee.html', {'employee': employee})

@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'inventory/customer_list.html', {'customers': customers})

@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'inventory/order_list.html', {'orders': orders})
