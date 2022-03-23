from django.views.generic import View
from rest_framework import status, viewsets
from rest_framework.response import Response


class CustomServiceViewset(viewsets.GenericViewSet):

    def service_create_or_destroy(self, service_name, obj):
        user = self.request.user
        serializer = super().get_serializer(obj, data=self.request.data)
        serializer.is_valid(raise_exception=True)
        obj_in_service = getattr(obj, service_name)
        if self.request.method == 'POST':
            obj_in_service.create(user_id=user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        obj_in_service.filter(user_id=user.id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def http_methods_except(method):
    return [m for m in View.http_method_names if m != method.lower()]
