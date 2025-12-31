from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from ...models import User
from rest_framework_simplejwt.tokens import RefreshToken


@csrf_exempt
@require_http_methods(["GET"])
def user_list(request):
    users = User.objects.filter(active=True).values(
        'id', 'name', 'email', 'created_date', 'updated_date', 'active')
    print(users)
    return JsonResponse(list(users), safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def user_create(request):
    try:
        data = json.loads(request.body)
        user = User.objects.create(
            name=data['name'],
            email=data['email'],
            password=data['password']
        )
        return JsonResponse({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'created_date': user.created_date.isoformat(),
            'updated_date': user.updated_date.strftime('%d/%m/%Y'),
            'active': user.active
        }, status=201)
    except KeyError as e:
        return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk, active=True)
        return JsonResponse({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'created_date': user.created_date.isoformat(),
            'updated_date': user.updated_date.isoformat(),
            'active': user.active
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


@csrf_exempt
@require_http_methods(["PUT"])
def user_update(request, pk):
    try:
        user = User.objects.get(pk=pk, active=True)
        data = json.loads(request.body)
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.password = data.get('password', user.password)
        user.active = data.get('active', user.active)
        user.save()
        return JsonResponse({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'created_date': user.created_date.isoformat(),
            'updated_date': user.updated_date.isoformat(),
            'active': user.active
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def user_delete(request, pk):
    try:
        user = User.objects.get(pk=pk, active=True)
        user.active = False
        user.save()
        return JsonResponse({'message': 'User deactivated successfully'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def user_login(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return JsonResponse({'error': 'Email and password are required'}, status=400)

        try:
            user = User.objects.get(email=email, active=True)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Cedenciales invalidas'}, status=401)

        if user.password != password:
            return JsonResponse({'error': 'Cedenciales invalidas'}, status=401)

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
