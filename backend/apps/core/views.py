from django.views.generic import View
from rest_framework import status
from rest_framework.response import Response


def http_methods_except(method):
    return [m for m in View.http_method_names if m != method.lower()]


class CreateDestroyServiceMixin:

    def service_create_or_destroy(self):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=self.request.data)
        serializer.is_valid(raise_exception=True)
        obj_in_service = getattr(obj, self.action)
        if self.request.method == 'POST':
            obj_in_service.create(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        obj_in_service.filter(user=self.request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
