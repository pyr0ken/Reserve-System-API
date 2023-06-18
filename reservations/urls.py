from django.urls import path, include
from . import views

api_url = [
    # path('table/week/<int:week_number>/', views.ReservationsAPIView.as_view(), name='reservations_list_api'),
]

app_name = 'reservations'
urlpatterns = [
    path('api/', include(api_url)),
    path("table/week/<int:week_number>/", views.ReservationsView.as_view(), name="table"),
    path("table/payment/", views.PaymentView.as_view(), name="payment"),
    path("table/payment/verify", views.PaymentView.as_view(), name="payment"),
]
