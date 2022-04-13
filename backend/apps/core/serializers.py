from rest_framework import serializers


class CustomServiceSerializer(serializers.ModelSerializer):

    def validate(self, data):
        obj = self.instance
        user = self.context['request'].user
        obj_in_service = getattr(obj, self.context['view'].action)
        has_user_obj = obj_in_service.filter(user=user).exists()
        request_method = self.context['request'].method
        if request_method == 'POST' and has_user_obj:
            raise serializers.ValidationError('Объект уже в списке!')
        elif request_method == 'DELETE' and not has_user_obj:
            raise serializers.ValidationError('Объекта нет в списке!')
        return data
