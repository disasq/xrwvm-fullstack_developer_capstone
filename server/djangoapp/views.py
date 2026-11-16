import json
from functools import wraps
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import CarMake, CarModel
from .restapis import get_request, post_review, analyze_review_sentiments


def api_errors(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        try:
            return view(*args, **kwargs)
        except (json.JSONDecodeError, KeyError, ValueError) as exc:
            return JsonResponse({'error': str(exc)}, status=400)
        except requests.RequestException:
            return JsonResponse({'error': 'Backend service unavailable'}, status=502)
    return wrapped


@require_http_methods(['POST'])
@api_errors
def login_user(request):
    data = json.loads(request.body)
    user = authenticate(request, username=data['userName'], password=data['password'])
    if user is None:
        return JsonResponse({'status': 'Invalid credentials'}, status=401)
    login(request, user)
    return JsonResponse({'userName': user.username, 'status': 'Authenticated',
                         'firstName': user.first_name, 'lastName': user.last_name})


@require_http_methods(['GET', 'POST'])
def logout_request(request):
    logout(request)
    return JsonResponse({'status': 'Logged out'})


@require_http_methods(['POST'])
@api_errors
def registration(request):
    data = json.loads(request.body)
    if not all(data.get(k) for k in ['userName', 'firstName', 'lastName', 'email', 'password']):
        return JsonResponse({'error': 'All five fields are required'}, status=400)
    try:
        user = User.objects.create_user(username=data['userName'], password=data['password'],
            email=data['email'], first_name=data['firstName'], last_name=data['lastName'])
    except IntegrityError:
        return JsonResponse({'error': 'Username already exists'}, status=409)
    login(request, user)
    return JsonResponse({'userName': user.username, 'status': 'Authenticated',
                         'firstName': user.first_name, 'lastName': user.last_name}, status=201)


@api_errors
def get_dealerships(request, state='All'):
    endpoint = 'fetchDealers' if state == 'All' else f'fetchDealers/{state}'
    return JsonResponse({'status': 200, 'dealers': get_request(endpoint)})


@api_errors
def get_dealer_details(request, dealer_id):
    dealer = get_request(f'fetchDealer/{dealer_id}')
    return JsonResponse({'status': 200, 'dealer': dealer})


@api_errors
def get_dealer_reviews(request, dealer_id):
    reviews = get_request(f'fetchReviews/dealer/{dealer_id}')
    for review in reviews:
        review['sentiment'] = analyze_review_sentiments(review['review'])['sentiment']
    return JsonResponse({'status': 200, 'reviews': reviews})


@require_http_methods(['POST'])
@api_errors
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login required'}, status=401)
    data = json.loads(request.body)
    data['name'] = request.user.get_full_name() or request.user.username
    return JsonResponse({'status': 200, 'review': post_review(data)})


def get_cars(request):
    cars = [{'CarMake': car.car_make.name, 'CarModel': car.name, 'Year': car.year}
            for car in CarModel.objects.select_related('car_make').all()]
    return JsonResponse({'status': 200, 'CarMakes': list(CarMake.objects.values('id', 'name', 'description')),
                         'CarModels': cars})
