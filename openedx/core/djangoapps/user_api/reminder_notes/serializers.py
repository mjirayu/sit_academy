from rest_framework import serializers

from student.models import ReminderNote


class ReminderNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReminderNote
        fields = ('id', 'user', 'text')
