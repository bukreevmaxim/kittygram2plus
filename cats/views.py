from rest_framework import viewsets
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from cats.pagination import CatsPagination
from cats.throttling import WorkingHoursRateThrottle
from .models import Achievement, Cat, User
from .permissions import OwnerOrReadOnly, ReadOnly
from .serializers import AchievementSerializer, CatSerializer, UserSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    # Добавим в кортеж ещё один бэкенд
    filter_backends = (DjangoFilterBackend, SearchFilter)
    pagination_class = None
    filterset_fields = ('color', 'birth_year')
    search_fields = ('^name', 'color', 'owner__username') 

    # def get_queryset(self):
    #     queryset = Cat.objects.all()
    #     # Добыть параметр color из GET-запроса
    #     color = self.request.query_params.get('color')
    #     if color is not None:
    #         #  через ORM отфильтровать объекты модели Cat
    #         #  по значению параметра color, полученного в запросе
    #         queryset = queryset.filter(color=color)
    #     return queryset

    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернём обновлённый перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer