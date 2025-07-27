from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from .models import Conversation


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow access only to participants of a conversation.
    For conversation-level objects.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user in obj.participants.all()


class IsParticipantInConversation(permissions.BasePermission):
    """
    Allow access only to participants in a given conversation (via conversation_pk).
    For message-level views.
    """

    def has_permission(self, request, view):
        conversation_id = view.kwargs.get("conversation_pk")
        if not conversation_id or not request.user.is_authenticated:
            return False

        try:
            conversation = Conversation.objects.get(pk=conversation_id)
        except Conversation.DoesNotExist:
            raise PermissionDenied("Conversation not found.")

        if request.user not in conversation.participants.all():
            raise PermissionDenied("You are not allowed to access this conversation.")

        return True
