from rest_framework import serializers


class CustomServiceSerializer(serializers.ModelSerializer):

    def service_validate(self, data):
        obj = self.instance
        user = self.context['request'].user
        obj_in_service = getattr(obj, self.context['view'].action)
        user_obj = obj_in_service.filter(user_id=user.id).first()
        request_method = self.context['request'].method
        if request_method == 'POST' and user_obj:
            raise serializers.ValidationError('Объект уже в списке!')
        elif request_method == 'DELETE' and not user_obj:
            raise serializers.ValidationError('Объекта нет в списке!')
        return data
