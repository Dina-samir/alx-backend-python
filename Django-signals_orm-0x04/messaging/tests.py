from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class MessagingTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='alice')
        self.receiver = User.objects.create_user(username='bob')

    def test_notification_created(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hi")
        self.assertEqual(Notification.objects.filter(user=self.receiver).count(), 1)

    def test_message_edit_creates_history(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Original")
        msg.content = "Edited"
        msg.save()
        self.assertTrue(msg.edited)
        self.assertEqual(msg.histories.count(), 1)

    def test_unread_manager(self):
        Message.objects.create(sender=self.sender, receiver=self.receiver, content="Msg 1")
        unread = Message.unread.for_user(self.receiver)
        self.assertEqual(unread.count(), 1)
