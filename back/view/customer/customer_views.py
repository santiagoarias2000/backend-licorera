from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from ...models import Customer

@csrf_exempt
@require_http_methods(["GET"])
def customer_list(request):
    customers = Customer.objects.all().values('id', 'name', 'document_type', 'document_number', 'birthdate', 'address', 'entry_date', 'created_date', 'updated_date', 'delivered')
    return JsonResponse(list(customers), safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def customer_create(request):
    try:
        data = json.loads(request.body)
        customer = Customer.objects.create(
            name=data['name'],
            document_type=data['document_type'],
            document_number=data['document_number'],
            birthdate=data['birthdate'],
            address=data['address']
        )
        return JsonResponse({
            'id': customer.id,
            'name': customer.name,
            'document_type': customer.document_type,
            'document_number': customer.document_number,
            'birthdate': customer.birthdate.isoformat(),
            'address': customer.address,
            'entry_date': customer.entry_date.isoformat(),
            'created_date': customer.created_date.isoformat(),
            'updated_date': customer.updated_date.isoformat(),
            'delivered': customer.delivered
        }, status=201)
    except KeyError as e:
        return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def customer_detail(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
        return JsonResponse({
            'id': customer.id,
            'name': customer.name,
            'document_type': customer.document_type,
            'document_number': customer.document_number,
            'birthdate': customer.birthdate.isoformat(),
            'address': customer.address,
            'entry_date': customer.entry_date.isoformat(),
            'created_date': customer.created_date.isoformat(),
            'updated_date': customer.updated_date.isoformat(),
            'delivered': customer.delivered
        })
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)

@csrf_exempt
@require_http_methods(["PUT"])
def customer_update(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
        data = json.loads(request.body)
        customer.name = data.get('name', customer.name)
        customer.document_type = data.get('document_type', customer.document_type)
        customer.document_number = data.get('document_number', customer.document_number)
        customer.birthdate = data.get('birthdate', customer.birthdate)
        customer.address = data.get('address', customer.address)
        customer.delivered = data.get('delivered', customer.delivered)
        customer.save()
        return JsonResponse({
            'id': customer.id,
            'name': customer.name,
            'document_type': customer.document_type,
            'document_number': customer.document_number,
            'birthdate': customer.birthdate.isoformat(),
            'address': customer.address,
            'entry_date': customer.entry_date.isoformat(),
            'created_date': customer.created_date.isoformat(),
            'updated_date': customer.updated_date.isoformat(),
            'delivered': customer.delivered
        })
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def customer_delete(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
        customer.delete()
        return JsonResponse({'message': 'Customer deleted successfully'})
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)