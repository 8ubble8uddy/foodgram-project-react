from djoser.views import UserViewSet

from api.users.serializers import CustomUserSerializer

from core.pagination import CustomPagination
from core.permissions import UserPermission


class CustomUserViewSet(UserViewSet):
    pagination_class = CustomPagination
    serializer_class = CustomUserSerializer
    permission_classes = (UserPermission,)
