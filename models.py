from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone

class Sleep_Data(models.Model):
    name = models.CharField(max_length=200)
    data_a = models.BigIntegerField()
    data_b = models.BigIntegerField()
    data_c = models.BigIntegerField()
    data_d = models.BigIntegerField()
    data_e = models.BigIntegerField()
    data_f = models.BigIntegerField()
    #published_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        #self.published_date = timezone.now()
        self.save()
    def __str__(self):
        return self.name
