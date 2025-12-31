from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import json
from ...models import Product


@csrf_exempt
@require_http_methods(["GET"])
def product_list(request):
    products = Product.objects.filter(active=True).values(
        'id', 'name', 'description', 'price', 'category', 'stock', 'size', 'active', 'created_date', 'updated_date')
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return JsonResponse(list(page_obj.object_list), safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def product_list_liquars(request):
    products = Product.objects.filter(active=True, category="LICORES").values(
        'id', 'name', 'description', 'price', 'category', 'stock', 'size', 'active', 'created_date', 'updated_date')
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return JsonResponse(list(page_obj.object_list), safe=False)

@csrf_exempt
@require_http_methods(["GET"])
def product_list_beer(request):
    products = Product.objects.filter(active=True, category="CERVEZAS").values(
        'id', 'name', 'description', 'price', 'category', 'stock', 'size', 'active', 'created_date', 'updated_date', "imagen")
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return JsonResponse(list(page_obj.object_list), safe=False)

@csrf_exempt
@require_http_methods(["GET"])
def product_list_otros(request):
    products = Product.objects.filter(active=True, category="OTROS").values(
        'id', 'name', 'description', 'price', 'category', 'stock', 'size', 'active', 'created_date', 'updated_date')
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return JsonResponse(list(page_obj.object_list), safe=False)

@csrf_exempt
@require_http_methods(["GET"])
def product_list_candy(request):
    products = Product.objects.filter(active=True, category="GOLOSINAS").values(
        'id', 'name', 'description', 'price', 'category', 'stock', 'size', 'active', 'created_date', 'updated_date')
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return JsonResponse(list(page_obj.object_list), safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def product_create(request):
    try:
        data = json.loads(request.body)
        product = Product.objects.create(
            name=data['name'],
            description=data.get('description'),
            price=data['price'],
            category=data['category'],
            stock=data.get('stock', 0),
            size=data.get('size'),
            imagen=data.get('image_url')
        )
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': str(product.price),
            'category': product.category,
            'stock': product.stock,
            'size': product.size,
            'active': product.active,
            'created_date': product.created_date.isoformat(),
            'updated_date': product.updated_date.isoformat()
        }, status=201)
    except KeyError as e:
        return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk, active=True)
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': str(product.price),
            'product_type': product.product_type,
            'category': product.category,
            'stock': product.stock,
            'size': product.size,
            'active': product.active,
            'created_date': product.created_date.isoformat(),
            'updated_date': product.updated_date.isoformat()
        })
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)


@csrf_exempt
@require_http_methods(["PUT"])
def product_update(request, pk):
    try:
        product = Product.objects.get(pk=pk, active=True)
        data = json.loads(request.body)
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.product_type = data.get('product_type', product.product_type)
        product.category = data.get('category', product.category)
        product.stock = data.get('stock', product.stock)
        product.size = data.get('size', product.size)
        product.active = data.get('active', product.active)
        product.save()
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': str(product.price),
            'product_type': product.product_type,
            'category': product.category,
            'stock': product.stock,
            'size': product.size,
            'active': product.active,
            'created_date': product.created_date.isoformat(),
            'updated_date': product.updated_date.isoformat()
        })
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def product_delete(request, pk):
    try:
        product = Product.objects.get(pk=pk, active=True)
        product.active = False
        product.save()
        return JsonResponse({'message': 'Product deactivated successfully'})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def product_random_by_category(request, category):
    try:
        # Validate category
        valid_categories = [choice[0] for choice in Product.CATEGORY_CHOICES]
        if category.upper() not in valid_categories:
            return JsonResponse({'error': 'Invalid category'}, status=400)

        # Get 6 random products from the category
        products = Product.objects.filter(
            active=True, category=category.upper()).order_by('?')[:6]
        product_list = []
        for product in products:
            product_list.append({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': str(product.price),
                'category': product.category,
                'stock': product.stock,
                'size': product.size,
                'active': product.active,
                'created_date': product.created_date.isoformat(),
                'updated_date': product.updated_date.isoformat()
            })
        return JsonResponse(product_list, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
