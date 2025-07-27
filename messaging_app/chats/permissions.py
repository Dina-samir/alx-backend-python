from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from .models import Conversation


class IsParticipantOfConversation(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (
            request.method in ["PUT", "PATCH", "DELETE"]
            and request.user.is_authenticated
        ):
            return False
        return request.user in obj.participants.all()


class IsParticipantInConversation(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        conversation_id = view.kwargs.get("conversation_pk")
        if not conversation_id or not request.user.is_authenticated:
            return False
        try:
            conversation = Conversation.objects.get(pk=conversation_id)
        except Conversation.DoesNotExist:
            raise PermissionDenied("Conversation not found.")

        if request.user in conversation.participants.all():
            return True

        raise PermissionDenied("You are not allowed to access this conversation.")