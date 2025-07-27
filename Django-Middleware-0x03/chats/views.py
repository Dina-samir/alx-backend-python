# chats/views.py

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Conversation, Message, CustomUser
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsParticipantOfConversation, IsParticipantInConversation


from .permissions import IsParticipantOfConversation
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter
from rest_framework.permissions import IsAuthenticated


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):
    #queryset = Message.objects.all().order_by('-timestamp')
    queryset = Message.objects.all().order_by('-sent_at')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__email', 'participants__first_name', 'participants__last_name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participants', [])

        if not participant_ids or len(participant_ids) < 2:
            return Response(
                {"detail": "At least two participants are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        participants = CustomUser.objects.filter(user_id__in=participant_ids)
        if participants.count() != len(participant_ids):
            return Response(
                {"detail": "One or more participant IDs are invalid."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body', 'sender__email']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']
    permission_classes = [IsAuthenticated, IsParticipantInConversation]

    def get_queryset(self):
        conversation_id = self.kwargs.get("conversation_pk")
        return Message.objects.filter(
            conversation_id=conversation_id,
            conversation__participants=self.request.user
        )

    def create(self, request, *args, **kwargs):
        conversation_id = self.kwargs.get("conversation_pk")
        sender_id = request.data.get("sender")
        message_body = request.data.get("message_body")

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        sender = get_object_or_404(CustomUser, user_id=sender_id)

        if sender not in conversation.participants.all():
            return Response(
                {"detail": "Sender is not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        message = Message.objects.create(
            sender=sender,
            conversation=conversation,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
