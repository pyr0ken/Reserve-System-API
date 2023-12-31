from django.urls import path, include
from . import views

api_url = [
    # path('table/week/<int:week_number>/', views.ReservationsAPIView.as_view(), name='reservations_list_api'),
]

app_name = 'reservations'
urlpatterns = [
    path('api/', include(api_url)),
    path("table/week/<int:week_number>/", views.ReservationsTableView.as_view(), name="table"),
    path("reserve/<int:timestamp>/", views.ReservationsDetailView.as_view(),
         name="detail"),
    path("payment/request/", views.ReservationsPaymentView.as_view(),
         name="payment_request"),
    path("payment/verify/", views.ReservationsVerifyView.as_view(), name="payment_verify"),
]
