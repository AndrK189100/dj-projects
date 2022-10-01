# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView

from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView, CreateAPIView, ListAPIView
from .models import Measurements, Sensor
from .serializers import SensorModelSerializer, MeasurementModelSerializer, SensorDetailSerializer


class SensorsListCreateAPIView(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorModelSerializer


class SensorsRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SensorDetailSerializer
        else:
            return SensorModelSerializer

    queryset = Sensor.objects.all()
    serializer_class = get_serializer_class


class MeasurementCreateAPIView(CreateAPIView):
    serializer_class = MeasurementModelSerializer

