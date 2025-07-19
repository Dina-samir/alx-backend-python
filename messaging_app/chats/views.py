# chats/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message, CustomUser
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participants', [])

        if not participant_ids or len(participant_ids) < 2:
            return Response({"detail": "At least two participants are required."}, status=status.HTTP_400_BAD_REQUEST)

        participants = CustomUser.objects.filter(user_id__in=participant_ids)
        if participants.count() != len(participant_ids):
            return Response({"detail": "One or more participant IDs are invalid."}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')
        return Message.objects.filter(conversation_id=conversation_id)

    def create(self, request, *args, **kwargs):
        conversation_id = self.kwargs.get('conversation_pk')
        sender_id = request.data.get('sender')
        message_body = request.data.get('message_body')

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        sender = get_object_or_404(CustomUser, user_id=sender_id)

        if sender not in conversation.participants.all():
            return Response({"detail": "Sender is not a participant in this conversation."}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            sender=sender,
            conversation=conversation,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
