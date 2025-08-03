from django.urls import path
from chats.views import message_list
from messaging.views import delete_user

urlpatterns = [
    path('messages/<int:user_id>/', message_list),
    path('delete-user/<int:user_id>/', delete_user),
]
