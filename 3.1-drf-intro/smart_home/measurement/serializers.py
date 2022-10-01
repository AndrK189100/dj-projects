from rest_framework import serializers

# TODO: опишите необходимые сериализаторы
from measurement.models import Measurements, Sensor


class SensorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'model', 'description']


class MeasurementModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurements
        fields = ['sensor', 'temp', 'date', 'image']


class MeasurementModelSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Measurements
        fields = ['temp', 'date', 'image']


class SensorDetailSerializer(serializers.ModelSerializer):
    measurements = MeasurementModelSerializer2(many=True, read_only=True)

    class Meta:
        model = Sensor
        fields = ['id', 'model', 'description', 'measurements']
