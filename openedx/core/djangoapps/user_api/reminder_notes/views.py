from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from openedx.core.lib.api.authentication import (
    SessionAuthenticationAllowInactiveUser,
    OAuth2AuthenticationAllowInactiveUser,
)
from openedx.core.lib.api.permissions import IsUserInUrlOrStaff
from openedx.core.lib.api.parsers import MergePatchParser
from student.models import UserProfile, ReminderNote
from .serializers import ReminderNoteSerializer


class ReminderNoteView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        reminder_notes = ReminderNote.objects.filter(
            user_id=request.user.id
        )

        serializer = ReminderNoteSerializer(reminder_notes, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.DATA
        data['user'] = request.user.id
        serializer = ReminderNoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReminderNoteDetailView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        try:
            reminder_note = ReminderNote.objects.get(
                id=pk,
                user_id=request.user.id
            )
        except ReminderNote.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ReminderNoteSerializer(reminder_note)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            reminder_note = ReminderNote.objects.get(
                id=pk,
                user_id=request.user.id
            )
        except ReminderNote.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.DATA
        data['user'] = request.user.id
        serializer = ReminderNoteSerializer(reminder_note, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            reminder_note = ReminderNote.objects.get(
                id=pk,
                user_id=request.user.id
            )
        except ReminderNote.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        reminder_note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
