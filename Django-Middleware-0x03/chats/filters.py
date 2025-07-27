# chats/filters.py

import django_filters
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    recipient = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    timestamp_after = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    timestamp_before = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'timestamp_after', 'timestamp_before']
