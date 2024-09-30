from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from django.db.models import ExpressionWrapper, F, FloatField

from .models import Category, Tag, Product, ProductFavorite, Color, Size
from .forms import AddToCartForm, LoginForm, RegisterForm
from payment.utils import CartForAuthenticated


# Create your views here.
def index_view(request):
    tags = Tag.objects.all()
    best_products = Product.objects.order_by('-sales')[:6]

    context = {
        'title': 'Главная страница',
        'tags': tags,
        'products': best_products
    }
    return render(request, 'pages/index.html', context)


class ProductFilter:
    def __init__(self, request, queryset):
        self.request = request
        self.queryset = queryset

    def filter_by_category(self):
        category = self.request.GET.get('category')
        if category:
            self.queryset = self.queryset.filter(category__id=category)
        return self

    def filter_by_brand(self):
        brand = self.request.GET.get('brand')
        if brand:
            self.queryset = self.queryset.filter(brand__id=brand)
        return self

    def filter_by_tag(self):
        tag = self.request.GET.get('tag')
        if tag:
            self.queryset = self.queryset.filter(tags__id=tag)
        return self

    def sort_by(self):
        sort = self.request.GET.get('sort')
        if sort:
            self.queryset = self.queryset.order_by(sort)
        return self

    def paginate(self):
        page = self.request.GET.get('page', 1)
        paginator = Paginator(self.queryset, 1)
        return paginator.get_page(page)

    def filter_by_price(self):
        price = self.request.GET.get('price')

        self.queryset = self.queryset.annotate(
            discount_price=ExpressionWrapper(
                F('price') - F('price') * F('discount') / 100.0,
                output_field=FloatField()
            )
        )

        if price:
            if price == '0_10':
                self.queryset = self.queryset.filter(discount_price__lt=10)
            elif price == '10_20':
                self.queryset = self.queryset.filter(discount_price__gte=10, discount_price__lt=20)
            elif price == '20_30':
                self.queryset = self.queryset.filter(discount_price__gte=20, discount_price__lt=30)
            elif price == '30_40':
                self.queryset = self.queryset.filter(discount_price__gte=30, discount_price__lt=40)
            elif price == '40_50':
                self.queryset = self.queryset.filter(discount_price__gte=40, discount_price__lt=50)
            elif price == 'more_50':
                self.queryset = self.queryset.filter(discount_price__gt=50)
        return self

    def get_queryset(self):
        return self.queryset


def shop_view(request):
    products = Product.objects.all()
    products_filter = ProductFilter(request, products)
    products = (products_filter
                .filter_by_category()
                .filter_by_brand()
                .filter_by_tag()
                .filter_by_price()
                .sort_by()
                .get_queryset())

    paginated_products = products_filter.paginate()
    context = {
        'title': 'Каталог',
        'products': paginated_products
    }
    return render(request, 'pages/shop.html', context)


def single_product(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        if request.method == 'POST':
            form = AddToCartForm(product)
            data = request.POST

            color = data.get('color')
            size = data.get('size')
            quantity = data.get('quantity')
            try:
                color = Color.objects.get(pk=int(color))
                size = Size.objects.get(pk=int(size))
            except:
                pass

            if size and color and quantity:
                CartForAuthenticated(request, product.pk, quantity, 'add', color.title, size.title)
                return redirect('product_path', slug)
            else:
                CartForAuthenticated(request, product.pk, 1, 'add')
                return redirect('product_path', slug)
        else:
            form = AddToCartForm(product)

        context = {
            'title': product.title,
            'product': product,
            'form': form
        }
        return render(request, 'pages/single-product.html', context)
    except Exception as error:
        print(error)
        return render(request, 'pages/error.html', context={'title': 'Ошибка'})


def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()

            if user:
                login(request, user)
                return redirect('index_path')
            else:
                return redirect('account_path')


def register_view(request):
    if request.method == 'POST':
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid():
            user = register_form.save()
            return redirect('index_path')
        else:
            return redirect('account_path')


def logout_view(request):
    logout(request)
    return redirect('index_path')


def account_view(request):
    login_form = LoginForm()
    register_form = RegisterForm()

    context = {
        'title': 'Аккаунт',
        'login_form': login_form,
        'register_form': register_form
    }
    return render(request, 'pages/account.html', context)


def favorite_activate(request, product_pk):
    user = request.user
    product = Product.objects.get(pk=product_pk)

    status = ProductFavorite.objects.filter(auth=user, product_id=product.pk).exists()

    if status is True:
        favorite = ProductFavorite.objects.get(auth=user, product_id=product.pk)
        favorite.delete()
    else:
        favorite = ProductFavorite.objects.create(auth=user, product_id=product.pk)
        favorite.save()

    return redirect(request.META.get('HTTP_REFERER', 'index_path'))


def favorite_view(request):
    user = request.user
    favorite_list = ProductFavorite.objects.filter(auth=user)
    context = {
        'title': 'Избранное',
        'favorite_list': favorite_list
    }
    return render(request, 'pages/wishlist.html', context)

