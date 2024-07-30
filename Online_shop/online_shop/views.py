from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Product, Category, Comment


def category(request, foo):
    foo = foo.replace('_', ' ')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
    except Category.DoesNotExist:
        messages.success(request, 'That category does not exist!')
        return redirect('home')
    return render(request, 'online_shop/category.html', {'category': category, 'products': products})


def home(request):
    products = Product.objects.all()
    return render(request, 'online_shop/home.html', {'products': products})


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'online_shop/detail.html', {'product': product})


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        comment_text = request.POST.get('text')
        if comment_text:
            comment = Comment(text=comment_text, product=product)
            comment.save()
            return redirect('product_detail', pk=product.pk)

    comments = product.comments.all()
    return render(request, 'online_shop/detail.html', {'product': product, 'comments': comments})
