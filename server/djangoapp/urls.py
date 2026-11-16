from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_user),
    path('logout', views.logout_request),
    path('register', views.registration),
    path('get_dealers', views.get_dealerships),
    path('get_dealers/<str:state>', views.get_dealerships),
    path('dealer/<int:dealer_id>', views.get_dealer_details),
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews),
    path('add_review', views.add_review),
    path('get_cars', views.get_cars),
]
