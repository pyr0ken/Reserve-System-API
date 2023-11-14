from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path('GetReservationWeek/<int:week_number>', views.GetReservationWeek.as_view(), name='GetReservationWeek'),
    path("GetReservationDetail/<str:reserve_date>/<str:reserve_time>/", views.GetReservationsDetail.as_view(),
         name="detail"),
]
