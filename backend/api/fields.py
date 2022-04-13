from rest_framework import fields


class ServiceSerializerField(fields.Field):
    def __init__(self, service, **kwargs):
        self.service = service
        kwargs['source'] = '*'
        kwargs['read_only'] = True
        super().__init__(**kwargs)

    def to_representation(self, obj):
        user = self.context['request'].user
        obj_in_service = getattr(obj, self.service)
        return (
            user.is_authenticated and
            user != obj and
            obj_in_service.filter(user_id=user.id).exists()
            )
