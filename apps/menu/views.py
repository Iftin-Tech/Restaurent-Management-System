from django.shortcuts import render, redirect
from apps.accounts.permissions import requires_permission
from .models import MenuCategory, MenuItem
from .forms import MenuCategoryForm, MenuItemForm

@requires_permission('manage_menu')
def category_list(request):
    categories = MenuCategory.objects.all().order_by('name')
    return render(request, 'menu/category_list.html', {'categories': categories})

@requires_permission('manage_menu')
def item_list(request):
    items = MenuItem.objects.all().select_related('category').order_by('name')
    return render(request, 'menu/item_list.html', {'items': items})

@requires_permission('manage_menu')
def category_create(request):
    if request.method == 'POST':
        form = MenuCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu:category_list')
    else:
        form = MenuCategoryForm()
    return render(request, 'menu/category_form.html', {'form': form, 'title': 'Add Category'})

@requires_permission('manage_menu')
def item_create(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu:item_list')
    else:
        form = MenuItemForm()
    return render(request, 'menu/item_form.html', {'form': form, 'title': 'Add Product Item'})
