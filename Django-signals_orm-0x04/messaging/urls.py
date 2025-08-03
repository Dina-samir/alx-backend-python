from django.urls import path
from chats.views import message_list
from messaging.views import delete_user
from . import views

# urlpatterns = [
#     path('messages/<int:user_id>/', message_list),
#     path('delete-user/<int:user_id>/', delete_user),
# ]

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('sent/', views.sent_messages, name='sent_messages'),
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
    path('send/', views.send_message, name='send_message'),
    path('notifications/', views.notifications, name='notifications'),
    path('delete-account/', views.delete_user, name='delete_user'),
]