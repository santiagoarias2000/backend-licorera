from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from ...models import Payment

@csrf_exempt
@require_http_methods(["GET"])
def payment_list(request):
    payments = Payment.objects.all().values('id', 'customer', 'product', 'amount', 'payment_method', 'created_date', 'updated_date', 'paid')
    return JsonResponse(list(payments), safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def payment_create(request):
    try:
        data = json.loads(request.body)
        payment = Payment.objects.create(
            customer_id=data['customer_id'],
            product_id=data['product_id'],
            amount=data['amount'],
            payment_method=data['payment_method']
        )
        return JsonResponse({
            'id': payment.id,
            'customer': payment.customer_id,
            'product': payment.product_id,
            'amount': str(payment.amount),
            'payment_method': payment.payment_method,
            'created_date': payment.created_date.isoformat(),
            'updated_date': payment.updated_date.isoformat(),
            'paid': payment.paid
        }, status=201)
    except KeyError as e:
        return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def payment_detail(request, pk):
    try:
        payment = Payment.objects.get(pk=pk)
        return JsonResponse({
            'id': payment.id,
            'customer': payment.customer_id,
            'product': payment.product_id,
            'amount': str(payment.amount),
            'payment_method': payment.payment_method,
            'created_date': payment.created_date.isoformat(),
            'updated_date': payment.updated_date.isoformat(),
            'paid': payment.paid
        })
    except Payment.DoesNotExist:
        return JsonResponse({'error': 'Payment not found'}, status=404)

@csrf_exempt
@require_http_methods(["PUT"])
def payment_update(request, pk):
    try:
        payment = Payment.objects.get(pk=pk)
        data = json.loads(request.body)
        payment.customer_id = data.get('customer_id', payment.customer_id)
        payment.product_id = data.get('product_id', payment.product_id)
        payment.amount = data.get('amount', payment.amount)
        payment.payment_method = data.get('payment_method', payment.payment_method)
        payment.paid = data.get('paid', payment.paid)
        payment.save()
        return JsonResponse({
            'id': payment.id,
            'customer': payment.customer_id,
            'product': payment.product_id,
            'amount': str(payment.amount),
            'payment_method': payment.payment_method,
            'created_date': payment.created_date.isoformat(),
            'updated_date': payment.updated_date.isoformat(),
            'paid': payment.paid
        })
    except Payment.DoesNotExist:
        return JsonResponse({'error': 'Payment not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def payment_delete(request, pk):
    try:
        payment = Payment.objects.get(pk=pk)
        payment.delete()
        return JsonResponse({'message': 'Payment deleted successfully'})
    except Payment.DoesNotExist:
        return JsonResponse({'error': 'Payment not found'}, status=404)