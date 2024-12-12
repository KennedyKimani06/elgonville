from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import InventoryItem, Supplier, Employee, Customer, Order, OrderItem
from .forms import InventoryItemForm, SupplierForm, EmployeeForm, CustomerForm, OrderForm, OrderItemForm


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
    suppliers = Supplier.objects.all()
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory:inventory_list')
    else:
        form = InventoryItemForm()
    return render(request, 'inventory/add_inventory.html', {'form': form, 'suppliers': suppliers})


@login_required
def edit_inventory(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    suppliers = Supplier.objects.all()
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('inventory:inventory_list')
    else:
        form = InventoryItemForm(instance=item)
    return render(request, 'inventory/edit_inventory.html', {'form': form, 'suppliers': suppliers})


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
    return render(request, 'inventory/employee_list.html',
                  {'employees': employees, 'customers': Customer.objects.all(), 'orders': Order.objects.all()})


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
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory:customer_list')
    else:
        form = CustomerForm()
    return render(request, 'inventory/add_customer.html', {'form': form})


@login_required
def edit_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('inventory:customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'inventory/edit_customer.html', {'form': form})


@login_required
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('inventory:customer_list')
    return render(request, 'inventory/delete_customer.html', {'customer': customer})


@login_required
def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            total_amount = 0
            for i in range(len(request.POST.getlist('items[0][inventory_item]'))):
                inventory_item_id = request.POST.getlist(f'items[{i}][inventory_item]')[0]
                quantity = int(request.POST.getlist(f'items[{i}][quantity]')[0])
                inventory_item = get_object_or_404(InventoryItem, id=inventory_item_id)
                price_per_unit = inventory_item.price_per_unit
                total_price = price_per_unit * quantity
                total_amount += total_price

                order_item = OrderItem(
                    order=order,
                    inventory_item=inventory_item,
                    quantity=quantity,
                    price=total_price
                )
                order_item.save()
            order.total_amount = total_amount
            order.save()
            return redirect('inventory:order_list')
    else:
        form = OrderForm()
    return render(request, 'inventory/add_order.html',
                  {'form': form, 'customers': Customer.objects.all(), 'inventory_items': InventoryItem.objects.all()})


@login_required
def edit_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            total_amount = 0
            OrderItem.objects.filter(order=order).delete()  # Remove old order items
            for i in range(len(request.POST.getlist('items[0][inventory_item]'))):
                inventory_item_id = request.POST.getlist(f'items[{i}][inventory_item]')[0]
                quantity = int(request.POST.getlist(f'items[{i}][quantity]')[0])
                inventory_item = get_object_or_404(InventoryItem, id=inventory_item_id)
                price_per_unit = inventory_item.price_per_unit
                total_price = price_per_unit * quantity
                total_amount += total_price

                order_item = OrderItem(
                    order=order,
                    inventory_item=inventory_item,
                    quantity=quantity,
                    price=total_price
                )
                order_item.save()
            order.total_amount = total_amount
            order.save()
            return redirect('inventory:order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'inventory/edit_order.html',
                  {'form': form, 'customers': Customer.objects.all(), 'inventory_items': InventoryItem.objects.all(),
                   'order': order})


@login_required
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('inventory:order_list')
    return render(request, 'inventory/delete_order.html', {'order': order})


@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'inventory/customer_list.html', {'customers': customers})


@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'inventory/order_list.html', {'orders': orders})
