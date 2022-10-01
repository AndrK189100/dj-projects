from django.db import models


# TODO: опишите модели датчика (Sensor) и измерения (Measurement)

class Sensor(models.Model):
    model = models.CharField(max_length=256, verbose_name='Наименование')
    description = models.CharField(max_length=256, null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.s_model


class Measurements(models.Model):
    sensor = models.ForeignKey(Sensor, related_name='measurements', on_delete=models.CASCADE)
    temp = models.FloatField(verbose_name='Температура')
    date = models.DateTimeField(verbose_name='Дата измерения', auto_now_add=True)
    image = models.ImageField(null=True, blank=True)
