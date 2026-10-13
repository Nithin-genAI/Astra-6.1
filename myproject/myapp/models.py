from django.db import models
#Model 1 for Item class Its like schema design ~
class Item(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


