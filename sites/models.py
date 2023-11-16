from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Website(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    name = models.CharField(max_length=100)

    clicks = models.PositiveIntegerField(default=0)
    data_sent = models.FloatField(default=0)
    data_received = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def increment_clicks(self):
        self.clicks += 1
        self.save()

    def update_data_sent(self, sent_amount):
        self.data_sent += sent_amount
        self.save()

    def update_data_received(self, received_amount):
        self.data_received += received_amount
        self.save()

    def get_absolute_url(self):
        return reverse('website:proxy', kwargs={'user_site_name': self.name, 'routes_on_original_site': self.url})

