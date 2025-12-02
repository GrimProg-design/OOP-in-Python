import time
from queue import PriorityQueue

class Notification:
    def __init__(self, title, message, priority=1, category='general', recipients=None):
        self.title = title
        self.message = message
        self.priority = priority
        self.category = category
        self.recipients = recipients or []
        self.timestamp = time.time()

    def is_urgent(self):
        return self.priority >= 5
    
    def get_summary(self):
        return f"{self.title}: {self.message[:20]}..."
    
    def __lt__(self, other):
        return self.priority > other.priority
    
class DeliveryChannel:
    def send(self, notification, recipient):
        raise NotImplementedError
    
    def can_send(self, notification):
        return True
    
class EmailChannel(DeliveryChannel):
    def send(self, notification, recipient):
        print(f"[Email] To {recipient}: {notification.get_summary()}")

class SMSChannel(DeliveryChannel):
    def send(self, notification, recipient):
        print(f"[SMS] To {recipient}: {notification.get_summary()}")

class PushChannel(DeliveryChannel):
    def send(self, notification, recipient):
        print(f"[Push] To {recipient}: {notification.get_summary()}")

class NotificationDecorator(Notification):
    def __init__(self, notification):
        self._notification = notification

    def __getattr__(self, name):
        return getattr(self._notification, name)

class LoggingDecorator(NotificationDecorator):
    def get_summary(self):
        print(f"[Log] Notification '{self._notification.title}' accessed")
        return self._notification.get_summary()
    
class Subscriber:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.channels = []
        self.preferences = {}

    def set_channel_preference(self, category, channel):
        self.preferences[category] = channel

class NotificationCenter:
    def __init__(self):
        self.subscribers = []
        self.channels = []
        self.queue = PriorityQueue()

    def register_subscriber(self, sub):
        self.subscribers.append(sub)

    def register_channel(self, channel):
        self.channels.append(channel)

    def add_notification(self, notification):
        self.queue.put(notification)

    def notify(self):
        while not self.queue.empty():
            notif = self.queue.get()
            for sub in self.subscribers:
                if notif.category in sub.preferences:
                    channel = sub.preferences[notif.category]
                else:
                    channel = self.channels[0]
                if channel.can_send(notif):
                    channel.send(notif, sub.name)

email = EmailChannel()
sms = SMSChannel()
push = PushChannel()

center = NotificationCenter()
center.register_channel(email)
center.register_channel(sms)
center.register_channel(push)

alice = Subscriber(1, "Alice")
bob = Subscriber(2, "Bob")

alice.set_channel_preference("urgent", sms)
bob.set_channel_preference("general", email)

center.register_subscriber(alice)
center.register_subscriber(bob)

n1 = LoggingDecorator(Notification("Hello", "This is a test message", priority=5, category="urgent"))
n2 = Notification("News", "Regular news update", priority=2, category="general")

center.add_notification(n1)
center.add_notification(n2)

center.notify()