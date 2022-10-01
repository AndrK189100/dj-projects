from django.urls import path

from measurement.views import SensorsListCreateAPIView, SensorsRetrieveUpdateAPIView, MeasurementCreateAPIView

urlpatterns = [
    # TODO: зарегистрируйте необходимые маршруты
    path('sensors/', SensorsListCreateAPIView().as_view()),
    path('sensors/<int:pk>/', SensorsRetrieveUpdateAPIView.as_view()),
    path('measurements/', MeasurementCreateAPIView.as_view())

]
