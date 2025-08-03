# messaging/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message, Notification
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone

@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user).select_related('sender').order_by('-timestamp')
    messages = messages.only('id', 'content', 'timestamp')
    return render(request, 'messaging/inbox.html', {'messages': messages})

@login_required
def unread_messages_view(request):
    unread_messages = Message.unread.unread_for_user(request.user)
    return render(request, 'messaging/unread.html', {'unread_messages': unread_messages})

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    # Mark as read if receiver is the viewer
    if message.receiver == request.user and not message.read:
        message.read = True
        message.save()

    return render(request, 'messaging/message_detail.html', {'message': message})

@login_required
@require_POST
def send_message(request):
    receiver_id = request.POST.get('receiver_id')
    content = request.POST.get('content')
    receiver = get_object_or_404(User, id=receiver_id)

    message = Message.objects.create(
        sender=request.user,
        receiver=receiver,
        content=content
    )

    return redirect('inbox')

@login_required
def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user).select_related('message').order_by('-created_at')
    return render(request, 'messaging/notifications.html', {'notifications': user_notifications})
