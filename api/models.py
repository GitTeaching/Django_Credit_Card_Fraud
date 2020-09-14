from django.db import models


# Not used in views
class ArrayData(models.Model):
  array_data = models.CharField(max_length=500)
      
  def __str__(self):
    return self.array_data
