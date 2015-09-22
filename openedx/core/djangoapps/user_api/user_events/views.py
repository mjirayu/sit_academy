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
from student.models import UserProfile, UserEvent
from .serializers import UserEventSerializer


class UserEventView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        events = UserEvent.objects.filter(
            user_id=request.user.id
        )

        serializer = UserEventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.DATA
        data['user'] = request.user.id
        serializer = UserEventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserEventDetailView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        try:
            event = UserEvent.objects.get(
                id=pk,
                user_id=request.user.id
            )
        except UserEvent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserEventSerializer(event)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            event = UserEvent.objects.get(
                id=pk,
                user_id=request.user.id
            )
        except UserEvent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.DATA
        data['user'] = request.user.id
        serializer = UserEventSerializer(event, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            event = UserEvent.objects.get(
                id=pk,
                user_id=request.user.id
            )
        except UserEvent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
