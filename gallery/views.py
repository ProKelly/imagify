from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView,CreateView, DeleteView
from .models import Product
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from .forms import ProductForm, LoginForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def ProductListView(request):
    products = Product.objects.all()
    q = request.GET.get('q', '')
    if q:
        products = Product.objects.filter(name__icontains=q)
    context = {'products':products}
    return render(request,  'gallery/product_list.html', context)

@method_decorator(login_required(login_url='login'), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'gallery/product_detail.html'
    context_object_name = 'product'

    def get_object(self):
        obj = super().get_object()
        obj.visited = timezone.now()
        return obj

@method_decorator(login_required(login_url='login'), name='dispatch')
class ProductCreateView(View):
    form_class = ProductForm
    template_name = 'gallery/form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form':form}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product-list')
        context = {'form':form}
        return render(request, self.template_name, context)
    
@login_required(login_url='login')
def product_edit_view(request, pk):
    product = Product.objects.get(pk=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product-list')
    context = {'form':form}
    return render(request, 'gallery/form.html', context)

@login_required(login_url='login')
def product_delete(request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return redirect('product-list')


def create_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            return redirect('product-list')
    context = {'form':form}
    return render(request, 'gallery/signup.html', context)

def login_user(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('product-list')
            else:
                messages.error(request, 'invalid user credentials')
    context = {'form':form}
    return render(request, 'gallery/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('product-list')