from rest_framework import serializers
from .models import ArrayData


# Not used in views 
class DataSerializer(serializers.ModelSerializer):
	class Meta:
		model = ArrayData
		fields ='__all__'