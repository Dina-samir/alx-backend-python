# chats/serializers.py

from rest_framework import serializers
from .models import CustomUser, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone_number',
            'role',
            'created_at'
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    message_body = serializers.CharField(max_length=1000)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_name', 'message_body', 'sent_at']

    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty or just whitespace.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']
