from rest_framework import serializers

from student.models import UserEvent


class UserEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEvent
        fields = ('id', 'user', 'title', 'start', 'end', 'color')
