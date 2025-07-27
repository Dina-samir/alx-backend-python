from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from .models import Conversation
from rest_framework.status import HTTP_403_FORBIDDEN

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow access only to participants of a conversation.
    Disallow updates and deletes for now.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.method in ["PUT", "PATCH", "DELETE"]:
            raise PermissionDenied("You cannot modify this conversation.")
        
        if not obj.sender == request.user or obj.recipient == request.user:
            raise PermissionDenied(detail="You are not allowed to view this message.", code=HTTP_403_FORBIDDEN)
        
        return request.user in obj.participants.all()


        
class IsParticipantInConversation(permissions.BasePermission):
    """
    Allow access only to participants in a given conversation (via conversation_pk).
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
