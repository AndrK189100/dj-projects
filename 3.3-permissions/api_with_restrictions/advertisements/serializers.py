from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, AdvFavorite


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',)

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # TODO: добавьте требуемую валидацию

        if self.context['view'].action in ['update', 'partial_update'] and 'status' in data \
                and data['status'] == 'OPEN':

            adv_status = Advertisement.objects.get(pk=self.context['view'].kwargs['pk']).status
            if adv_status == 'CLOSED':
                query = Advertisement.objects.filter(creator=self.context['request'].user, status='OPEN').count()
                if query >= 3:
                    raise ValidationError('To many OPEN advertisements')

        elif self.context['view'].action == 'create' and ('status' not in data or data['status'] == 'OPEN'):
            query = Advertisement.objects.filter(creator=self.context['request'].user, status='OPEN').count()
            if query >= 3:
                raise ValidationError('To many OPEN advertisements')

        return data


class AdvFavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdvFavorite
        fields = ['fv_users', 'advertisements']

