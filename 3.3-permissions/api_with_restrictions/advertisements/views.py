from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, AdvFavorite
from advertisements.permissions import IsOwner
from advertisements.serializers import AdvertisementSerializer, AdvFavoriteSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    authentication_classes = [TokenAuthentication]

    queryset = Advertisement.objects.all()

    def get_queryset(self):

        user = self.request.user

        if user.is_anonymous:
            return self.queryset.filter(status='OPEN')
        elif user.is_superuser:
            return self.queryset
        else:
            res1 = self.queryset.filter(creator=user, status='CLOSED')
            res2 = self.queryset.filter(status='OPEN')
            return res1.union(res2)

    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwner()]
        if self.action == 'make_favorite':
            return [IsAuthenticated()]
        return []

    @action(detail=True, methods=['post'])
    def make_favorite(self, request, pk=None):
        user = request.user.id
        data = {'fv_users': user, 'advertisements': int(pk)}

        serializer = AdvFavoriteSerializer(data=data)

        if serializer.is_valid():

            if AdvFavorite.objects.filter(fv_users=user, advertisements=int(pk)):
                raise ValidationError('has already')

            if Advertisement.objects.get(creator=user, pk=pk):
                raise ValidationError('You are owner)')

            serializer.save()
            return Response({'status': 'OK'})
        else:
            raise ValidationError('No found')
