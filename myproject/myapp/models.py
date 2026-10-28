from django.db import models
#Model 1 for Item class Its like schema design ~
class Item(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.category}"
    


